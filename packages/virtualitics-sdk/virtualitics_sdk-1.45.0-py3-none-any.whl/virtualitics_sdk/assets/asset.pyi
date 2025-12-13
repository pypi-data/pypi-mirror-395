from _typeshed import Incomplete
from enum import Enum, StrEnum
from io import StringIO as StringIO
from predict_backend.validation.type_validation import validate_types
from typing import Any

logger: Incomplete

class AssetType(Enum):
    MODEL: str
    NLPROCESSOR: str
    SCHEMA: str
    DATASET: str
    KNOWLEDGE_GRAPH: str
    OTHER: str
    DATASTORE: str

class AssetPersistenceMethod(StrEnum):
    PICKLE: str
    CSV: str
    EXCEL: str
    JSON: str
    BYTES: str
    PARQUET: str

class Asset:
    '''
    Class for storing objects along with their metadata. Supported object types are AssetTypes.
    Assets are created by specifying the type of object being stored and a label for the object.
    The label is intended to describe objects relevant to a specific project, an example would be
    \'Jet Engine subsystem N41\'. An additional name can be specified to differentiate between different
    versions of a specific object. Assets can be stored and retrieved through the store interface.
    Assets also allow users to write any notes/important information relevant to an object.
    They can also be linked to other persistence or asset objects, such as linking a model
    to the dataset it was trained on. 

    The `type` field describes what kind of object is being stored. Please see the
    :class:`~virtualitics_sdk.assets.asset.AssetType` class for the full list of available AssetTypes. In order to
    store a generic python object, please create an asset with this class with type `AssetType.OTHER`. 
    
    :param object: The object which is stored by the asset.
    :param label: Label for the object, can be used later to identify the object.
    :param type: The type of object being stored. 
    :param metadata: Any additional metadata to be stored along with the object.
    :param name: Identifier to differentiate Assets with the same label.
    :param description: A description of the asset.
    :param version: Version of the asset.

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import Asset, AssetType
           . . .
           # Example usage
           acc = Asset(object=[1, 2, 3], label="ex", type=AssetType.OTHER, name="ex-1")
           store_interface.save_asset(acc)
    '''
    object: Incomplete
    label: Incomplete
    type: Incomplete
    id: Incomplete
    time_created: Incomplete
    name: Incomplete
    metadata: Incomplete
    description: Incomplete
    version: Incomplete
    linked_asset_objects: dict[str, str]
    user_notes: Incomplete
    engineer_notes: Incomplete
    time_to_live: Incomplete
    @validate_types
    def __init__(self, object: Any, label: str, type: AssetType, metadata: dict | None = None, name: str | None = None, description: str | None = None, version: int | None = None, **kwargs) -> None: ...
    def get_object(self) -> Any: ...
    def set_time_to_live(self, time_to_live) -> None: ...
    def set_description(self, description: str) -> None: ...
    def link_asset(self, label: str, asset: Asset) -> None:
        '''
            Function to link asset to other persistence objects. 
            Example use case: linking a model to its training dataset.
            model_asset = asset(...)
            model_asset.link_asset("training dataset", X_train_asset)
        '''
    def add_notes(self, dict_type: str, key: str | None = None, notes: str | None = None) -> None:
        """
            Add key value pair to specified notes dictionary. If key is not specified,
            notes is assumed to be text written by the engineer which is added to a log.
        """
    def add_engineer_notes(self, key: str | None = None, notes: str | None = None) -> None: ...
    def add_user_notes(self, key: str | None = None, notes: str | None = None) -> None: ...
    def __eq__(self, other: Asset) -> bool:
        """Equality method for comparing Assets.
           Checks equivalence of asset attributes, does not do a
           deep equality check of stored object, just checks for same type
           and attributes.
        """
    @classmethod
    def from_metadata(cls, asset_metadata, asset_object, training_data=None): ...
    def to_bytes(self, serialization_method: AssetPersistenceMethod) -> bytes: ...
    @staticmethod
    def from_bytes(payload, encrypted: bool, serialization_method: AssetPersistenceMethod, asset_type) -> Any: ...

def update_asset(asset: Asset) -> Asset: ...
