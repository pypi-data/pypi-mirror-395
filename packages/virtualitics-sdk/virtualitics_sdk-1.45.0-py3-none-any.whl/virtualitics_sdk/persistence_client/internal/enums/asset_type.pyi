from _typeshed import Incomplete
from enum import Enum

class PersistenceAssetType(Enum):
    """List of possible asset types"""
    INVALID: Incomplete
    PROJECT: Incomplete
    DATASET: Incomplete
    OBJECT: Incomplete
    SETTINGS: Incomplete
    WORKFLOW: Incomplete
    @classmethod
    def from_str(self, string): ...
