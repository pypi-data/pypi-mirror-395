from datetime import datetime
from typing import Any
from virtualitics_sdk.persistence_client.internal.dataclasses.request_parameters import GetMetaDataParameters as GetMetaDataParameters
from virtualitics_sdk.persistence_client.internal.enums.asset_type import PersistenceAssetType as PersistenceAssetType

class PersistenceMetadata(dict):
    """
    Contains metadata pointing to a file on persistence.
    Crucial part of the PersistenceClient system. Used as
    the output and input of most PersistenceClient calls.
    
    WARNING: This object is READ ONLY, changing fields only reflects
    locally and could cause unexpected behavior. Use PersistenceClient
    to change metadata of persistence files.
    """
    def __init__(self, persistence_client: Any, **kwargs) -> None: ...
    @property
    def asset_id(self) -> str | None: ...
    @property
    def user_id(self) -> str | None: ...
    @property
    def asset_type(self) -> str | None: ...
    @property
    def created_at(self) -> datetime | None: ...
    @property
    def updated_at(self) -> datetime | None: ...
    @property
    def file_name(self) -> str | None: ...
    @property
    def description(self) -> str | None: ...
    @property
    def content_length(self) -> int | None: ...
    @property
    def file_extension(self) -> str | None: ...
    @classmethod
    def from_server_response(cls, data: dict[str, Any], persistence_client) -> PersistenceMetadata:
        """Creates a PersistenceMetadata object from the dictionary format returned by GET_META_DATA."""
    def copy(self, **changes) -> PersistenceMetadata:
        """Creates a shallow copy of this instance, optionally updating fields."""
