import hashlib
from datetime import datetime
from typing import List, Tuple

from wmain.core.http import Api, request
from wmain.common.models import BaseAliasModel


class Pan123File(BaseAliasModel):
    file_id: int
    filename: str
    parent_file_id: int  # 父级文件ID
    type: int  # 0-文件  1-文件夹
    etag: str  # md5
    size: int  # 文件大小 单位B
    status: int  # 文件审核状态。 大于 100 为审核驳回文件
    trashed: int
    create_at: datetime


class AccessToken(BaseAliasModel):
    access_token: str
    expired_at: datetime


class UploadInfo(BaseAliasModel):
    file_id: int
    completed: bool


class Pan123(Api):

    def __init__(self, client_id: str, client_secret: str):
        super().__init__(
            base_url="https://open-api.123pan.com",
            headers={
                "Platform": "open_platform",
                "Authorization": "{access_token}",
            }
        )
        self["access_token"] = None
        self["client_id"] = client_id
        self["client_secret"] = client_secret

    async def flush_access_token(self):
        access_token = await self.get_access_token()
        self["access_token"] = "Bearer " + access_token.access_token

    async def get_file_list(self,
                            parent_file_id: int = 0,
                            limit: int = 100,
                            last_file_id: int = None,
                            trashed=0) -> list[Pan123File]:
        resp = await self.api_get_file_list(
            parent_file_id=parent_file_id,
            limit=limit,
            last_file_id=last_file_id
        )
        return [
            file for file in
            [Pan123File.from_any_dict(item) for item in resp.json()["data"]["fileList"]]
            if file.trashed is None or file.trashed == trashed
        ]

    async def get_access_token(self) -> AccessToken:
        resp = await self.api_get_access_token()
        return AccessToken.from_any_dict(resp.json()["data"])

    async def get_upload_domain(self) -> List[str]:
        resp = await self.api_get_upload_domain()
        urls = resp.json()["data"]
        self["upload_url"] = urls[0]
        return urls

    async def upload_file_bytes(
            self,
            file_bytes: bytes,
            parent_file_id: int,
            filename: str,
            duplicate: int = 2,
            contain_dir: bool = False,
            upload_url: str = None
    ) -> UploadInfo:
        if upload_url is None:
            upload_urls = await self.get_upload_domain()
            upload_url = upload_urls[0]
        size = len(file_bytes)
        md5 = hashlib.md5(file_bytes).hexdigest()
        resp = await self.api_upload_file(
            parent_file_id=parent_file_id,
            size=size,
            md5=md5,
            filename=filename,
            file=(filename, file_bytes),
            duplicate=duplicate,
            contain_dir=contain_dir,
            upload_url=upload_url
        )
        return UploadInfo.from_any_dict(resp.json()["data"])

    async def get_download_url(self, file_id: int):
        return await self.api_get_file_download_info(file_id=file_id)

    async def download_file(self, file_id: int, local_filepath: str):
        resp = await self.get_download_url(file_id)
        download_url = resp.json()["data"]["downloadUrl"]
        with open(local_filepath, "wb+") as f:
            resp = await self.api_download_file(download_url)
            f.write(resp.content)

    @request("POST", "/api/v1/access_token",
             data={
                 "clientID": "{client_id}",
                 "clientSecret": "{client_secret}"
             })
    async def api_get_access_token(self):
        """
        获取 access_token
        """
        pass

    @request("GET", "/api/v1/file/download_info",
             params={
                 "fileId": "{file_id}"
             })
    async def api_get_file_download_info(self, file_id: int):
        """
        获取文件下载信息
        """
        pass

    @request("GET", "/api/v2/file/list",
             params={
                 "parentFileId": "{parent_file_id}",
                 "limit": "{limit}",
                 "searchData": "{search_data}",
                 "searchMode": "{search_mode}",
                 "lastFileId": "{last_file_id}"
             })
    async def api_get_file_list(self,
                                parent_file_id: int,
                                limit: int,
                                search_data: str = None,
                                search_mode: str = None,
                                last_file_id: int = None):
        """
        获取文件列表
        :param parent_file_id: 文件夹ID，根目录传 0
        :param limit: 每页文件数量，最大不超过100
        :param search_data:
            搜索关键字将无视文件夹ID参数。将会进行全局查找
        :param search_mode:
            0:全文模糊搜索(注:将会根据搜索项分词,查找出相似的匹配项)
            1:精准搜索(注:精准搜索需要提供完整的文件名)
        :param last_file_id:
            翻页查询时需要填写
        """
        pass

    @request("GET", "/upload/v2/file/domain")
    async def api_get_upload_domain(self):
        """
        获取上传域名
        """
        pass

    @request("POST", "{upload_url}/upload/v2/file/single/create",
             data={
                 "parentFileId": "{parent_file_id}",
                 "filename": "{filename}",
                 "size": "{size}",
                 "etag": "{md5}",
                 "duplicate": "{duplicate}",
                 "containDir": "{contain_dir}"
             },
             files={
                 "file": "{file}"
             })
    async def api_upload_file(self,
                              upload_url: str,
                              parent_file_id: int,
                              filename: str,
                              file: Tuple[str, bytes],
                              size: int,
                              md5: str,
                              duplicate: int = 2,
                              contain_dir: bool = False):
        """
        上传文件
        :param filename:
        :param upload_url:
        :param contain_dir:
            上传文件是否包含路径，默认false
        :param duplicate:
            非必填	当有相同文件名时，文件处理策略
            1 保留两者，新文件名将自动添加后缀
            2 覆盖原文件
        :param file: 文件名和文件字节的元组
        :param parent_file_id: 文件夹ID，根目录传 0
        :param size: 文件大小
        :param md5: 文件md5
        """
        pass

    @request("GET", "/api/v1/file/download_info",
             params={
                 "fileId": "{file_id}"
             })
    async def api_get_file_download_info(self, file_id: int):
        """
        获取文件下载信息
        """
        pass

    @request("GET", "{download_url}")
    async def api_download_file(self, download_url: str):
        """
        下载文件
        """
        pass

    @request("POST", "/upload/v1/file/mkdir",
             data={
                 "parentID": "{parent_id}",
                 "name": "{name}"
             })
    async def api_mkdir(self, parent_id: int, name: str):
        """
        创建文件夹
        """
        pass


async def test_async():
    pan123 = Pan123(
        client_id="65d555f6dd0d4560b64c73bb8b9f6ada",
        client_secret="0da30fec47844459a79f9b56740129a3",
    )
    await pan123.flush_access_token()
    # resp = await pan123.get_file_list()
    # await pan123.api_mkdir(parent_id=0, name="test")
    await pan123.upload_file_bytes(open("__init__.py", "rb").read(),
                                   0,
                                   "123.txt")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_async())
