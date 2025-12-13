import copy
import functools
import inspect
import json
import re
from typing import TypeVar, ParamSpec, Callable, Awaitable, Union

import httpx

from wmain.common.http import Url
from wmain.common.logging import HttpLogRecord
from wmain.common.utils import MuTree
from wmain.common.models import AutoMatchModel


class ApiException(Exception):
    """API 请求异常"""
    pass


class ResultTypeException(Exception):
    """API 返回结果类型错误"""
    pass


# 用于类型标注函数参数和返回值
P = ParamSpec("P")
R = TypeVar("R", bound=Union[httpx.Response, AutoMatchModel])


class Api:
    """
    Api 必须有一个init函数来初始化base_url等值
    """
    # 占位符正则，用于替换 URL 和请求体中的 {attr}
    PLACEHOLDER_PATTERN = re.compile(r"{(\w+)}")

    def __init__(self,
                 base_url: str = None,
                 client: httpx.Client = None,
                 async_client: httpx.AsyncClient = None,
                 headers: dict = None,
                 params: dict = None,
                 json: dict = None,
                 data: dict = None,
                 timeout: int = None,
                 log_callback: Callable = None):
        """
        初始化 API 实例
        - base_url: API 基础 URL
        - client / async_client: 可自定义 httpx 同步/异步客户端
        - headers / params / json / data: 默认请求参数
        - timeout: 请求超时时间
        - callback: 当请求后会将请求url,请求
        """
        self.base_url: Url = Url(base_url or "")
        self.headers: dict = headers or {}
        self.params: dict = params or {}
        self.json: dict = json or {}
        self.data: dict = data or {}
        self.timeout: int = timeout or None
        self.attrs: dict = {}  # 用于存放全局占位符值，例如 token
        self.log_callback: Callable = log_callback

        self.client: httpx.Client = client or httpx.Client(
            base_url=base_url, headers=headers, timeout=timeout
        )
        self.async_client: httpx.AsyncClient = async_client or httpx.AsyncClient(
            base_url=base_url, headers=headers, timeout=timeout,
            follow_redirects=True
        )

    def __setitem__(self, key, value):
        """可以用 c['token'] = 'xxx' 设置占位符"""
        self.attrs[key] = value

    def __getitem__(self, key):
        """获取占位符"""
        return self.attrs[key]

    def replace_placeholder(self,
                            obj: dict | list | tuple | str,
                            replace_dic: dict):
        """递归替换 任何可替换类型 中所有字符串值中的占位符"""
        mutree = MuTree(obj)

        for node in mutree.walk():

            if not node.is_leaf:
                continue

            if not isinstance(node.data, str):
                continue

            matches = self.PLACEHOLDER_PATTERN.findall(node.data)

            if not matches:
                continue

            # 情况1：整个字符串就是一个占位符，比如 "{id}"
            if len(matches) == 1 and node.data.strip() == f"{{{matches[0]}}}":
                name = matches[0]
                if name not in replace_dic:
                    raise ValueError(f"Missing value for placeholder '{name}'")
                node.data = replace_dic.get(name)
                if node.data is None:
                    node.delete()
                continue

            # 情况2：常规替换
            for name in matches:
                if name not in replace_dic:
                    raise ValueError(f"Missing value for placeholder '{name}'")
                value = replace_dic.get(name)
                node.data = node.data.replace(f"{{{name}}}", str(value))

        return mutree.get()

    def _prepare_request_kwargs(self, func, method, path_or_uri,
                                headers=None, params=None, json_data=None, data=None,
                                timeout=None, files=None, args=(), **kwargs):
        """
        核心方法：准备请求参数字典和客户端方法
        - 根据函数参数和全局 attrs 替换占位符
        - 返回 (client_method, req_kwargs, log)
        """
        # 绑定函数参数
        sig = inspect.signature(func)
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()

        # 深拷贝默认值
        final_headers = copy.deepcopy({**self.headers, **(headers or {})})
        final_params = copy.deepcopy({**self.params, **(params or {})})
        final_json = copy.deepcopy({**self.json, **(json_data or {})})
        final_data = copy.deepcopy({**self.data, **(data or {})})

        # 占位符替换字典：优先函数参数，其次全局 attrs
        replace_dic = {**self.attrs, **bound.arguments}

        # 替换请求体、参数、头部中的占位符
        final_headers, final_params, final_json, final_data, files = self.replace_placeholder(
            [final_headers, final_params, final_json, final_data, files],
            replace_dic
        )

        path_or_uri = self.replace_placeholder(path_or_uri, replace_dic)
        url = self.base_url.join(path_or_uri)
        final_url = self.replace_placeholder(str(url), replace_dic)

        # 构建请求参数字典
        req_kwargs = {
            "url": final_url,
            "headers": final_headers or None,
            "params": final_params or None,
            "json": final_json if method.lower() in ["post", "put", "patch"] else None,
            "data": final_data if method.lower() in ["post", "put", "patch"] else None,
            "timeout": timeout or self.timeout,
            "files": files or None
        }
        # 去掉值为 None 的项
        req_kwargs = {k: v for k, v in req_kwargs.items() if v is not None}

        # 获取对应客户端方法
        client_method = getattr(self.async_client if inspect.iscoroutinefunction(func)
                                else self.client, method.lower())

        # 构建日志
        log = None
        if self.log_callback:
            url_obj = Url(final_url)
            body_data = final_json or final_data or {}
            request_body_bytes = json.dumps(body_data).encode('utf-8') if body_data else b""
            log = HttpLogRecord(
                client="httpx",
                method=method.upper(),
                url=final_url,
                scheme=url_obj.scheme,
                host=url_obj.netloc or "",
                port=0,
                path=url_obj.path,
                query_string=url_obj.query,
                http_version="",
                request_headers=final_headers,
                request_body=request_body_bytes or b"",
            )

        return client_method, req_kwargs, log


def request(method: str,
            path_or_uri: str,
            headers=None,
            params=None,
            json=None,
            data=None,
            timeout=None,
            files=None,
            **httpx_kwargs):
    """
    通用装饰器
    - 支持同步函数和异步函数
    - 自动根据函数是否 async 决定使用 self.client 或 self.async_client
    - 自动执行 callback(log) 并填充请求和响应信息
    """

    def decorator(func: Callable[P, Union[R, Awaitable[R]]]) -> Callable[P, Union[R, Awaitable[R]]]:
        is_async = inspect.iscoroutinefunction(func)
        return_annotation = inspect.signature(func).return_annotation
        return_model = False
        if return_annotation is not httpx.Response and return_annotation is not inspect.Parameter.empty:
            if not issubclass(return_annotation, AutoMatchModel):
                raise ResultTypeException(
                    "The return type of the function must be httpx.Response "
                    "or AutoMatchModel"
                )
            else:
                return_model = True

        # 异步包装器
        @functools.wraps(func)
        async def async_wrapper(self: Api, *args: P.args, **kwargs) -> R:
            client_method, req_kwargs, log = self._prepare_request_kwargs(
                func, method, path_or_uri, headers, params, json, data,
                timeout, files, args, **kwargs
            )

            if self.log_callback:
                log.set_request_time()

            response: httpx.Response = await client_method(**{**req_kwargs, **httpx_kwargs})

            if self.log_callback:
                log.set_response_time()
                log.cal_duration()
                log.set_response(response)
                await self.log_callback(log)

            if return_model:
                return return_annotation(**response.json())
            return response

        # 同步包装器
        @functools.wraps(func)
        def sync_wrapper(self: Api, *args: P.args, **kwargs) -> R:
            client_method, req_kwargs, log = self._prepare_request_kwargs(
                func, method, path_or_uri, headers, params, json, data,
                timeout, files, args, **kwargs
            )

            if self.log_callback:
                log.set_request_time()

            response: httpx.Response = client_method(**{**req_kwargs, **httpx_kwargs})

            if self.log_callback:
                log.set_response(response)
                log.set_response_time()
                log.cal_duration()
                self.log_callback(log)

            if return_model:
                return return_annotation(**response.json())
            return response

        return async_wrapper if is_async else sync_wrapper

    return decorator
