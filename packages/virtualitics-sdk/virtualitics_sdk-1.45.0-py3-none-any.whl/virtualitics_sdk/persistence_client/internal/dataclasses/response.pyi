import httpx
from httpx import Response as Response
from pydantic import BaseModel
from typing import Any

class GetAssetResponse(BaseModel):
    content: bytes
    headers: dict[str, str]
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> GetAssetResponse: ...

class GetMetaDataResponse(BaseModel):
    json_list: list[dict[str, Any]] | None
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> GetMetaDataResponse: ...

class SaveAssetResponse(BaseModel):
    data: dict[str, Any]
    asset_id: str
    user_id: str
    asset_type: str
    content_length: int
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> SaveAssetResponse: ...

class UpdateMetaDataResponse(BaseModel):
    asset_id: str
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> UpdateMetaDataResponse: ...

class CopyAssetResponse(BaseModel):
    asset_id: str
    user_id: str
    asset_type: str
    content_length: int
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> CopyAssetResponse: ...

class DeleteAssetResponse(BaseModel):
    content: bytes | None
    status_code: int
    @staticmethod
    def parse_response(response: httpx.Response) -> DeleteAssetResponse: ...
