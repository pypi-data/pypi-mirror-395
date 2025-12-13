from datetime import datetime as datetime
from io import BytesIO as BytesIO
from pydantic import BaseModel
from typing import Any

class GetAssetParameters(BaseModel):
    asset_id: str
    def format(self) -> dict[str, Any]: ...

class SaveAssetParameters(BaseModel):
    asset_id: str
    asset_type: str
    file: tuple[str, BytesIO, str | None]
    def format(self) -> dict[str, Any]: ...
    class Config:
        arbitrary_types_allowed: bool

class GetMetaDataParameters(BaseModel):
    limit: int | None
    asset_id: str | None
    last_id: str | None
    asset_type: str | None
    created_after: datetime | None
    updated_after: datetime | None
    created_before: datetime | None
    updated_before: datetime | None
    size_greater_than: int | None
    size_less_than: int | None
    error_no_results: bool | None
    def format(self) -> dict[str, Any]: ...

class CopyAssetParameters(BaseModel):
    asset_id: str
    def format(self) -> dict[str, Any]: ...

class DeleteAssetParameters(BaseModel):
    asset_id: str
    def format(self) -> dict[str, Any]: ...

class UpdateMetaDataParameters(BaseModel):
    asset_id: str
    metadata: dict[str, Any]
    def format(self) -> dict[str, Any]: ...
