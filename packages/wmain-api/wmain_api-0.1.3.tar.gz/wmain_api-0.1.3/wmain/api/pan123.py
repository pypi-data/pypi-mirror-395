import asyncio
import hashlib
from datetime import datetime
from typing import List, Tuple, Optional, TypeVar, Any, Generator

from wmain.core.http import Api, request
from wmain.common.models import AutoMatchModel


class Pan123Exception(Exception):
    pass


class NoRequestUrlException(Pan123Exception):
    pass


class FileNotFoundException(Pan123Exception):
    pass


class Pan123File(AutoMatchModel):
    file_id: int
    filename: str
    parent_file_id: int  # 父级文件ID
    type: int  # 0-文件  1-文件夹
    etag: str  # md5
    size: int  # 文件大小 单位B
    status: int  # 文件审核状态。 大于 100 为审核驳回文件
    trashed: int
    create_at: datetime


class FileList(AutoMatchModel):
    last_file_id: int
    file_list: List[Pan123File]


class AccessToken(AutoMatchModel):
    access_token: str
    expired_at: datetime


class UploadResult(AutoMatchModel):
    file_id: int
    completed: bool


class VipInfo(AutoMatchModel):
    vip_level: int  # 1,2,3 = VIP / SVIP / 长期VIP
    vip_label: str  # VIP 级别名称
    start_time: datetime  # 开始时间
    end_time: datetime  # 结束时间


class DeveloperInfo(AutoMatchModel):
    start_time: datetime  # 开发者权益开始时间
    end_time: datetime  # 开发者权益结束时间


class UploadPart(AutoMatchModel):
    part_number: str
    size: int
    etag: str


class UploadParts(AutoMatchModel):
    parts: List[UploadPart]


class UserInfo(AutoMatchModel):
    uid: int  # 用户账号 id
    nickname: str  # 昵称
    head_image: str  # 头像
    passport: str  # 手机号码
    mail: str  # 邮箱

    space_used: int  # 已用空间
    space_permanent: int  # 永久空间
    space_temp: int  # 临时空间
    space_temp_expr: datetime  # 临时空间到期日

    vip: bool  # 是否会员
    direct_traffic: int  # 剩余直链流量
    is_hide_uid: bool  # 是否在直链中隐藏 UID
    https_count: int  # https 数量

    vip_info: List[VipInfo]
    developer_info: Optional[DeveloperInfo]


class MultiUploadInfo(AutoMatchModel):
    file_id: Optional[int]
    preupload_id: str
    reuse: bool
    slice_size: int
    servers: List[str]


T = TypeVar("T")


class ApiResponse(AutoMatchModel):
    code: int
    message: str
    data: Any = None
    x_trace_id: str

    def get_data_as(self, model_cls: type[T]) -> List[T] | T | None:
        """智能转换 data 字段"""
        if self.data is None:
            return None
        if isinstance(self.data, list):
            return [model_cls(**item) for item in self.data]
        if isinstance(self.data, dict):
            return model_cls(**self.data)
        return self.data  # str / int / bool 等原始类型直接返回


class UploadTask:

    def __init__(
            self,
            pan123: "Pan123",
            file_bytes: bytes,
            parent_file_id: int,
            filename: str,
            duplicate: int = 2,
            contain_dir: bool = False,
    ):
        self.pan123 = pan123
        self.file_bytes = file_bytes
        self.parent_file_id = parent_file_id
        self.filename = filename
        self.duplicate = duplicate
        self.contain_dir = contain_dir
        self.md5 = hashlib.md5(file_bytes).hexdigest()
        self.size = len(file_bytes)
        self.upload_info = None

    async def create(self) -> MultiUploadInfo:
        """返回 UploadInfo, 可通过reuse判断是否秒传"""
        resp = await self.pan123.api_upload_create_file(
            parent_file_id=self.parent_file_id,
            filename=self.filename,
            file=(self.filename, self.file_bytes),
            size=self.size,
            md5=self.md5,
            duplicate=self.duplicate,
            contain_dir=self.contain_dir,
        )
        self.upload_info = resp.get_data_as(MultiUploadInfo)
        return self.upload_info

    @property
    def chunks(self) -> Generator[bytes]:
        slice_size = self.upload_info.slice_size
        for start in range(0, self.size, slice_size):
            end = min(start + slice_size, self.size)  # 关键：不能越界！
            chunk = self.file_bytes[start:end]  # 保证最后一片不会是空
            yield chunk

    async def single_upload(self, upload_url: str = None) -> UploadResult:
        if not upload_url:
            upload_url = await self.pan123.get_any_upload_domain()
            if upload_url is None:
                raise NoRequestUrlException(
                    "upload servers is empty when single upload"
                )
        resp = await self.pan123.api_single_upload_file(
            parent_file_id=self.parent_file_id,
            filename=self.filename,
            file=(self.filename, self.file_bytes),
            size=self.size,
            md5=self.md5,
            duplicate=self.duplicate,
            contain_dir=self.contain_dir,
            upload_url=upload_url
        )
        return resp.get_data_as(UploadResult)

    async def multi_upload(self):
        if not self.upload_info.servers:
            raise NoRequestUrlException("Upload Servers is empty")
        tasks = [
            self.pan123.api_upload_slice(
                preupload_id=self.upload_info.preupload_id,
                chunk=(self.filename, chunk),
                chunk_no=chunk_no,
                chunk_md5=hashlib.md5(chunk).hexdigest(),
                upload_url=self.upload_info.servers[0]
            )
            for chunk_no, chunk in enumerate(self.chunks, start=1)
        ]
        await asyncio.gather(*tasks)

    async def complete(self) -> UploadResult:
        resp = await self.pan123.api_upload_complete(
            preupload_id=self.upload_info.preupload_id
        )
        return resp.get_data_as(UploadResult)


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

    async def refresh_access_token(self):
        resp = await self.api_get_access_token()
        self["access_token"] = "Bearer " + resp.get_data_as(AccessToken).access_token

    async def get_upload_domains(self) -> List[str]:
        resp = await self.api_get_upload_domain()
        return resp.data

    async def get_any_upload_domain(self) -> Optional[str]:
        upload_urls = await self.get_upload_domains()
        if not upload_urls:
            return None
        upload_url = upload_urls[0]
        return upload_url

    async def get_upload_task(
            self,
            file_bytes: bytes,
            parent_file_id: int,
            filename: str,
            duplicate: int = 2,
            contain_dir: bool = False,
    ) -> UploadTask:
        return UploadTask(
            pan123=self,
            file_bytes=file_bytes,
            parent_file_id=parent_file_id,
            filename=filename,
            duplicate=duplicate,
            contain_dir=contain_dir,
        )

    async def iter_file_list(
            self,
            parent_file_id: int,
            search_data: str = None,
            search_mode: int = None,
            limit: int = 100,
    ) -> Generator[Pan123File]:
        while True:
            resp = await self.api_get_file_list(
                parent_file_id=parent_file_id,
                limit=limit,
                search_data=search_data,
                search_mode=search_mode
            )
            file_list = resp.get_data_as(FileList)
            for file in file_list.files:
                yield file
            if file_list.last_file_id == -1:
                break

    async def download_file(self, file_id: int, local_filepath: str):
        resp = await self.api_get_file_download_info(file_id=file_id)
        if not resp.data:
            raise FileNotFoundException(f"file_id {file_id} not found")
        download_url = resp.data["downloadUrl"]
        with open(local_filepath, "wb+") as f:
            resp = await self.api_download_file(download_url)
            f.write(resp.content)

    @request("POST", "/api/v1/access_token",
             data={
                 "clientID": "{client_id}",
                 "clientSecret": "{client_secret}"
             })
    async def api_get_access_token(self) -> ApiResponse:
        """
        获取 access_token
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
    async def api_get_file_list(
            self,
            parent_file_id: int,
            limit: int,
            search_data: str = None,
            search_mode: str = None,
            last_file_id: int = None
    ) -> ApiResponse:
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
    async def api_get_upload_domain(self) -> ApiResponse:
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
    async def api_single_upload_file(
            self,
            upload_url: str,
            parent_file_id: int,
            filename: str,
            file: Tuple[str, bytes],
            size: int,
            md5: str,
            duplicate: int = 2,
            contain_dir: bool = False
    ) -> ApiResponse:
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

    @request("POST", "/upload/v2/file/create",
             data={
                 "parentFileId": "{parent_file_id}",
                 "filename": "{filename}",
                 "size": "{size}",
                 "etag": "{md5}",
                 "duplicate": "{duplicate}",
                 "containDir": "{contain_dir}"
             })
    async def api_upload_create_file(
            self,
            parent_file_id: int,
            filename: str,
            file: Tuple[str, bytes],
            size: int,
            md5: str,
            duplicate: int = 2,
            contain_dir: bool = False
    ) -> ApiResponse:
        """参数同上, 返回data为PreUploadInfo"""
        pass

    @request("POST", "{upload_url}/upload/v2/file/slice",
             data={
                 "preuploadID": "{preupload_id}",
                 "sliceNo": "{chunk_no}",
                 "sliceMD5": "{chunk_md5}",
             },
             files={
                 "slice": "{chunk}"
             })
    async def api_upload_slice(
            self,
            preupload_id: str,
            chunk_no: int,
            chunk_md5: str,
            chunk: Tuple[str, bytes],
            upload_url: str
    ):
        """

        :param upload_url:
        :param preupload_id:
        :param chunk_no: 分片编号, 从 1 开始
        :param chunk_md5:
        :param chunk:
        :return:
        """
        pass

    @request("POST", "/upload/v2/file/upload_complete",
             data={
                 "preuploadID": "{preupload_id}"
             })
    async def api_upload_complete(self, preupload_id: str) -> ApiResponse:
        pass

    @request("GET", "/api/v1/file/download_info",
             params={
                 "fileId": "{file_id}"
             })
    async def api_get_file_download_info(self, file_id: int) -> ApiResponse:
        pass

    @request("GET", "{download_url}")
    async def api_download_file(self, download_url: str):
        pass

    @request("POST", "/upload/v1/file/mkdir",
             data={
                 "parentID": "{parent_id}",
                 "name": "{name}"
             })
    async def api_mkdir(self, parent_id: int, name: str) -> ApiResponse:
        pass

    @request("GET", "/api/v1/user/info")
    async def api_get_user_info(self) -> ApiResponse:
        pass

    @request("GET", "/api/v1/file/detail",
             params={
                 "fileID": "{file_id}"
             })
    async def api_get_file_detail(self, file_id: int) -> ApiResponse:
        pass
