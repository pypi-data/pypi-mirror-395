from datetime import datetime
from typing import List, Tuple, Optional, TypeVar, Any, Generator

from wmain.core.http import Api
from wmain.common.models import AutoMatchModel


class Pan123Exception(Exception):
    ...


class NoRequestUrlException(Pan123Exception):
    ...


class Pan123File(AutoMatchModel):
    file_id: int
    filename: str
    parent_file_id: int
    type: int
    etag: str
    size: int
    status: int
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
    vip_level: int
    vip_label: str
    start_time: datetime
    end_time: datetime


class DeveloperInfo(AutoMatchModel):
    start_time: datetime
    end_time: datetime


class UploadPart(AutoMatchModel):
    part_number: str
    size: int
    etag: str


class UploadParts(AutoMatchModel):
    parts: List[UploadPart]


class UserInfo(AutoMatchModel):
    uid: int
    nickname: str
    head_image: str
    passport: str
    mail: str
    space_used: int
    space_permanent: int
    space_temp: int
    space_temp_expr: datetime
    vip: bool
    direct_traffic: int
    is_hide_uid: bool
    https_count: int
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
    data: Any
    x_trace_id: str
    def get_data_as(self, model_cls: type[T]) -> List[T] | T | None: ...


class UploadTask:
    pan123: "Pan123"
    file_bytes: bytes
    parent_file_id: int
    filename: str
    duplicate: int
    contain_dir: bool
    md5: str
    size: int
    upload_info: MultiUploadInfo | None
    def __init__(
            self,
            pan123: "Pan123",
            file_bytes: bytes,
            parent_file_id: int,
            filename: str,
            duplicate: int = 2,
            contain_dir: bool = False,
    ) -> None: ...
    async def create(self) -> MultiUploadInfo: ...
    @property
    def chunks(self) -> Generator[bytes, None, None]: ...
    async def single_upload(self, upload_url: str = None) -> UploadResult: ...
    async def multi_upload(self) -> None: ...
    async def complete(self) -> UploadResult: ...


class Pan123(Api):
    client_id: str
    client_secret: str
    def __init__(self, client_id: str, client_secret: str) -> None: ...
    async def refresh_access_token(self) -> None: ...
    async def get_upload_domains(self) -> List[str]: ...
    async def get_any_upload_domain(self) -> Optional[str]: ...
    async def get_upload_task(
            self,
            file_bytes: bytes,
            parent_file_id: int,
            filename: str,
            duplicate: int = 2,
            contain_dir: bool = False,
    ) -> UploadTask: ...
    async def iter_file_list(
            self,
            parent_file_id: int,
            search_data: str = None,
            search_mode: int = None,
            limit: int = 100,
    ) -> Generator[Pan123File]: ...
    async def download_file(self, file_id: int, local_filepath: str) -> None: ...
    async def api_get_access_token(self) -> ApiResponse: ...
    async def api_get_file_list(
            self,
            parent_file_id: int,
            limit: int,
            search_data: str = None,
            search_mode: str = None,
            last_file_id: int = None
    ) -> ApiResponse: ...
    async def api_get_upload_domain(self) -> ApiResponse: ...
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
    ) -> ApiResponse: ...
    async def api_upload_create_file(
            self,
            parent_file_id: int,
            filename: str,
            file: Tuple[str, bytes],
            size: int,
            md5: str,
            duplicate: int = 2,
            contain_dir: bool = False
    ) -> ApiResponse: ...
    async def api_upload_slice(
            self,
            preupload_id: str,
            chunk_no: int,
            chunk_md5: str,
            chunk: Tuple[str, bytes],
            upload_url: str
    ) -> None: ...
    async def api_upload_complete(self, preupload_id: str) -> ApiResponse: ...
    async def api_get_file_download_info(self, file_id: int) -> ApiResponse: ...
    async def api_download_file(self, download_url: str): ...
    async def api_mkdir(self, parent_id: int, name: str) -> ApiResponse: ...
    async def api_get_user_info(self) -> ApiResponse: ...
    async def api_get_file_detail(self, file_id: int) -> ApiResponse: ...


async def callback(msg) -> None: ...


async def test() -> None: ...