from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from virtualitics_sdk import DrilldownCallback as DrilldownCallback
from virtualitics_sdk.page.comment import Comment as Comment
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback, StandardEventCallback as StandardEventCallback

logger: Incomplete

class ElementHorizontalPosition(Enum):
    LEFT: str
    CENTER: str
    RIGHT: str

class ElementVerticalPosition(Enum):
    TOP: str
    CENTER: str
    BOTTOM: str

class ElementOverflowBehavior(Enum):
    SCROLL: str
    FIT: str
    FULLSIZE: str

class ElementType(Enum):
    TABLE: str
    DASHBOARD: str
    IMAGE: str
    FILTERS: str
    INPUT: str
    DROPDOWN: str
    DATE_TIME_RANGE: str
    NUMERIC_RANGE: str
    DATA_SOURCE: str
    TEXT_INPUT: str
    PLOT: str
    CUSTOM_EVENT: str
    INFOGRAPHIC: str
    INFOGRAPH_DATA: str
    RICH_TEXT: str
    XAI_DASHBOARD: str
    BUTTON: str

class Element(ABC):
    """An Element in the Virtualitics AI Platform.

        :param _type: The type of element.
        :param params: The parameters for that element.
        :param content: The content of the element.
        :param _id: The ID of the element, defaults to None.
        :param title: The title of the element, defaults to ''.
        :param description: The description of the element, defaults to ''.
        :param show_title: Whether to show the title on the page when rendered, defaults to True.
        :param show_description: Whether to show the description to the page when rendered, defaults to True.
        :param label: The label of the element, defaults to ''.
        :param placeholder: The placeholder of the element, defaults to ''.
        :param on_click: Callback used for clickable elements, defaults to None.
        :param horizontal_position: The horizontal position the element should be placed, defaults to ElementHorizontalPosition.LEFT
        :param vertical_position: The vertical position the element should be placed, defaults to ElementVerticalPosition.TOP
        :param overflow_behavior: For supported elements, specifies how the platform will handle the overflow of the content. Defaults to ElementOverflowBehavior.SCROLL
        :param reference_id: A user-defined reference ID for the unique identification of an element within the Page, defaults to ''.
    """
    id: Incomplete
    type: Incomplete
    card_id: str
    title: Incomplete
    description: Incomplete
    show_title: Incomplete
    show_description: Incomplete
    comments: list['Comment']
    label: Incomplete
    placeholder: Incomplete
    virtualitics_sdk_version: Incomplete
    on_click: Incomplete
    horizontal_position: Incomplete
    vertical_position: Incomplete
    overflow_behavior: Incomplete
    hash_bump: int
    reference_id: Incomplete
    def __init__(self, _type: ElementType, params: dict[str, Any], content: dict | list | str, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, _id: str = '', label: str = '', placeholder: str = '', on_click: DrilldownCallback | StandardEventCallback | PageUpdateCallback | None = None, horizontal_position: ElementHorizontalPosition = ..., vertical_position: ElementVerticalPosition = ..., overflow_behavior: ElementOverflowBehavior = ..., reference_id: str | None = '') -> None: ...
    def serialize_drilldown(self): ...
    def edit_comment(self, comment_id: str, new_comment_message: str, editor: str) -> Comment: ...
    def delete_comment(self, comment_id: str): ...
    def get_comment(self, comment_id: str) -> Comment: ...
    def to_json(self) -> dict:
        """Convert the element to a JSON.

        :return: A JSON dictionary of the element.
        """
    def extract_context(self): ...
    def add_comment(self, comment: Comment): ...

class InputElement(Element):
    has_updater: Incomplete
    updater_name: Incomplete
    page_update: Incomplete
    def __init__(self, _type: ElementType, params: dict, content: dict, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, label: str = '', placeholder: str = '', page_update: PageUpdateCallback | None = None, on_click: DrilldownCallback | StandardEventCallback | PageUpdateCallback | None = None, horizontal_position: ElementHorizontalPosition = ..., vertical_position: ElementVerticalPosition = ..., reference_id: str | None = '') -> None: ...
    @abstractmethod
    def get_value(self) -> str | dict | list[str]:
        """Get the value of an element. If the user has interacted with the value, the default
        will be updated.
        """
