import datetime
import httpx
from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum as Enum, auto as auto
from io import BytesIO
from pandas import DataFrame
from virtualitics.explore.workflow import Workflow
from virtualitics_sdk.exceptions.exception import PredictException as PredictException
from virtualitics_sdk.persistence_client.internal.auth.credential_provider import CredentialProvider as CredentialProvider
from virtualitics_sdk.persistence_client.internal.dataclasses.metadata import PersistenceMetadata as PersistenceMetadata
from virtualitics_sdk.persistence_client.internal.dataclasses.request_parameters import CopyAssetParameters as CopyAssetParameters, DeleteAssetParameters as DeleteAssetParameters, GetAssetParameters as GetAssetParameters, GetMetaDataParameters as GetMetaDataParameters, SaveAssetParameters as SaveAssetParameters, UpdateMetaDataParameters as UpdateMetaDataParameters
from virtualitics_sdk.persistence_client.internal.dataclasses.response import CopyAssetResponse as CopyAssetResponse, DeleteAssetResponse as DeleteAssetResponse, GetAssetResponse as GetAssetResponse, GetMetaDataResponse as GetMetaDataResponse, SaveAssetResponse as SaveAssetResponse, UpdateMetaDataResponse as UpdateMetaDataResponse
from virtualitics_sdk.persistence_client.internal.enums.asset_type import PersistenceAssetType as PersistenceAssetType
from virtualitics_sdk.persistence_client.internal.enums.request_type import RequestType as RequestType

jwt: Incomplete

@dataclass
class PersistenceClient:
    """
    Main class of PredictPersistence. Wraps a httpx.AsyncClient and httpx.Client 
    allowing users to send API requests to the Persistence server. Uses client_requests
    to handle the logic for sending each of these requests to the server.
    """
    async_client: httpx.AsyncClient
    client: httpx.Client
    credential_provider: CredentialProvider
    def __init__(self) -> None:
        """Initializes the client connection."""
    def convert_dict_to_metadata(self, raw_dict: dict): ...
    def build_explore_link(self, asset: PersistenceMetadata | str, workflow: PersistenceMetadata = None, force_load: bool = True, display_spreadsheet: bool = False) -> str:
        """
        build_explore_link creates a link to Virtualitics Explore that auto opens an asset based off the
        given parameters. 
        
        :param asset: can be either metadata of a persistence file or the string name of a sample project/dataset
        param workflow_metadata: optional metadata for a workflow file
        :param forceLoad:
        :param displaySpreadsheet:
        """
    def copy(self, metadata: PersistenceMetadata) -> PersistenceMetadata:
        """
        Copies the persistence file to a location and returns the metadata of the new file.
        
        :param metadata: the metadata of the asset we want to copy
        """
    def delete(self, metadata: PersistenceMetadata) -> bool:
        """
        Deletes the persistence file associated with the metadata and returns whether the action was
        successful or not.
        
        :param metadata: the metadata of the file you want to delete
        """
    def find(self, limit: int | None = None, asset_id: str | None = None, last_id: str | None = None, asset_type: PersistenceAssetType | None = None, created_after: datetime | None = None, updated_after: datetime | None = None, created_before: datetime | None = None, updated_before: datetime | None = None, error_no_results: bool | None = None) -> list[PersistenceMetadata]:
        """
        Finds all persistence metadata files that match the given filter parameters.

        :param limit: Maximum number of metadata entries to return.
        :param asset_id: If provided, filters results to a specific asset ID.
        :param last_id: Returns asset_ids greater than this value
        :param asset_type: Filter by the type of persistence asset (e.g., dataset, workflow).
        :param created_after: Only return assets created after this datetime.
        :param updated_after: Only return assets updated after this datetime.
        :param created_before: Only return assets created before this datetime.
        :param updated_before: Only return assets updated before this datetime.
        :param error_no_results: If True, raise an error when no matching assets are found; otherwise return an empty list.

        :return: A list of PersistenceMetadata objects that match the given criteria.
        """
    def get_content(self, metadata: PersistenceMetadata) -> bytes:
        """
        Returns the byte contents of a file identified by metadata.
        
        :param metadata: the metadata of the file you want to read
        """
    def rename(self, metadata: PersistenceMetadata, name: str | None = None, description: str | None = None) -> PersistenceMetadata:
        """
        Alters the metadata of the given file, giving it a new name and description. If no description or name
        given the file will retain its original name or description. Returns the altered version of the metadata.
        
        :param metadata: the metadata of the file you want to rename
        :param name: the new name of the file
        :param description: the new description of the file
        """
    def set_content(self, metadata: PersistenceMetadata, file: BytesIO | DataFrame, file_name: str = None, asset_type: PersistenceAssetType = None) -> PersistenceMetadata:
        """
        Puts specified content into an existing file. Used to save updated contents to
        a file already on Persistence. Name and type can be specified if they change.
        
        :param metadata: metadata of the file on the server we are changing
        :param file: the BytesIO or DataFrame file contents that will be uploaded
        :param file_name: the new name of the file
        :param asset_type: the new asset type of the file (there probably aren't that many uses for this)
        """
    def upload(self, file: BytesIO | DataFrame | Workflow, file_name: str, asset_type: PersistenceAssetType) -> PersistenceMetadata:
        """
        Uploads a file to Persistence and returns the metadata of the new Persistence file.
        Note that not all the fields of metadata will be returned using this method. Properties
        within the PersistenceMetadata class can lazily retrieve the missing data if needed.
        
        :param file: the BytesIO or DataFrame file contents that will be uploaded
        :param file_name: the name of the file
        :param asset_type: the type of asset of the file 
        """
    async def copy_async(self, metadata: PersistenceMetadata):
        """Asynchronous version of the copy function."""
    async def delete_async(self, metadata: PersistenceMetadata) -> bool:
        """Asynchronous version of the delete function."""
    async def find_async(self, limit: int | None = None, asset_id: str | None = None, last_id: str | None = None, asset_type: PersistenceAssetType | None = None, created_after: datetime | None = None, updated_after: datetime | None = None, created_before: datetime | None = None, updated_before: datetime | None = None, size_greater_than: int | None = None, size_less_than: int | None = None, error_no_results: bool | None = None) -> list[PersistenceMetadata]:
        """Asynchronous version of the find function."""
    async def get_content_async(self, metadata: PersistenceMetadata):
        """Asynchronous version of the get_content function."""
    async def rename_async(self, metadata: PersistenceMetadata, name: str, description: str = None) -> PersistenceMetadata:
        """Asynchronous version of the rename function."""
    async def set_content_async(self, metadata: PersistenceMetadata, file: BytesIO | DataFrame, file_name: str = None, asset_type: PersistenceAssetType = None):
        """Asynchronous version of the set_content function."""
    async def upload_async(self, file: BytesIO | DataFrame | Workflow, file_name: str, asset_type: PersistenceAssetType):
        """Uploads a file to persistence and returns the metadata of this file."""

def ensure_metadata(metadata) -> PersistenceMetadata: ...
def convert_to_bytesio(file) -> BytesIO: ...
