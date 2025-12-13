import time
from typing import Optional, Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, FileResponse

from wmain.common.logging import HttpLogRecord


def make_logging_middleware(
        callback: Callable[[HttpLogRecord], Awaitable[None]],
        max_body_size: int = 1024,
):
    class LoggingMiddleware(BaseHTTPMiddleware):

        async def dispatch(self, request: Request, call_next):
            req_ts = time.time()

            body_bytes: Optional[bytes] = await request.body()
            if body_bytes and len(body_bytes) > max_body_size:
                body_bytes = None

            # 支持 FastAPI 后续读取
            async def receive():
                return {
                    "type": "http.request",
                    "body": body_bytes or b"",
                    "more_body": False
                }

            request._receive = receive

            response = await call_next(request)

            resp_ts = time.time()

            response_bytes = None
            if not isinstance(response, (StreamingResponse, FileResponse)):
                collected = b""
                async for chunk in response.body_iterator:
                    collected += chunk
                if len(collected) <= max_body_size:
                    response_bytes = collected

                # 重置 body_iterator
                async def new_iter():
                    yield collected

                response.body_iterator = new_iter()

            # ------------------------- 构建 LogInfo -------------------------
            client = f"{request.client.host}:{request.client.port}" if request.client else None

            info = HttpLogRecord(
                client=client,
                method=request.method,
                url=str(request.url),
                scheme=request.url.scheme,
                host=request.url.hostname or "",
                port=request.url.port or 0,
                path=request.url.path,
                query_string=request.url.query or "",
                http_version=request.scope.get("http_version", ""),

                request_headers=dict(request.headers),
                request_body=body_bytes,

                response_status=response.status_code,
                response_headers=dict(response.headers),
                response_body=response_bytes,
            )
            info.set_request_response_time(req_ts, resp_ts)

            if callback:
                await callback(info)

            return response

    return LoggingMiddleware
