from enum import Enum
from typing import Any, Coroutine, Protocol
from virtualitics_sdk import Card as Card, DrilldownStoreInterface as DrilldownStoreInterface

class DrilldownType(Enum):
    FAST_MODAL: str
    MODAL: str
    POPOVER: str

class DrilldownSize(Enum):
    SMALL: str
    MEDIUM: str
    LARGE: str
    SHEET: str

class DrilldownCallback(Protocol):
    """
    Protocol defining the required callback signature.
    Any callable matching this signature can be used as a drilldown callback.
    """
    def __call__(self, card: Card, input_data: dict[str, str | float | int], store_interface: DrilldownStoreInterface, drilldown_type: DrilldownType = ..., drilldown_size: DrilldownSize = ...) -> Coroutine[Any, Any, None]:
        """
        Process drilldown data and add content to the card.

        :param card: Card object to add content to
        :param input_data: Dictionary containing input parameters related to the element that was engaged to trigger
                           this modal/popover
        :param store_interface: Optimal Interface for accessing persisted objects during modal/popover creation
        :param drilldown_type: DrilldownType.MODAL or DrilldownType.POPOVER
        :param drilldown_size: DrilldownSize.SMALL, MEDIUM, LARGE, SHEET
        """
