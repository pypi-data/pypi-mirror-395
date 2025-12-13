from _typeshed import Incomplete
from enum import Enum
from virtualitics_sdk.persistence_client.internal.enums.method import Method as Method

class RequestType(Enum):
    """Enumeration of possible persistence API actions."""
    GET_META_DATA: Incomplete
    GET_ASSET_DATA: Incomplete
    SAVE_ASSET: Incomplete
    DELETE_ASSET: Incomplete
    UPDATE_META_DATA: Incomplete
    COPY_ASSET: Incomplete

def get_route_and_method_info(requestType: RequestType): ...
