from _typeshed import Incomplete
from enum import Enum
from pydantic import BaseModel, computed_field
from typing import Literal
from virt_llm import AsyncLLMClient as AsyncLLMClient
from virtualitics_sdk.elements.element import Element as Element, ElementType as ElementType

logger: Incomplete

class RawChatContext(BaseModel):
    user_id: str
    app_id: str
    chat_id: str
    chat_index: int
    step_name: str
    element_id: str
    prompt: str
    llm_host: str
    model: str
    response: str | None
    llm_client: AsyncLLMClient | None
    model_config: Incomplete

class ProcessedChatMessage(BaseModel):
    role: Literal['user', 'system']
    content: str

class ChatSource(BaseModel):
    """Single Source.
    The source can be one of two types:
    - Link to a Predict Element (Table, Infographic, PlotlyPlot, Rich Text).
    You can create it by only passing the `page_element` param.
    - Custom. This will not be linked to any Predict Element. You must provide
    a valid `title` and `element_type`

    :param page_element: Optional. Reference of the source.
    :type page_element: Element | None
    :param title: Optional. Name of the source.
    :type title: str | None
    :param element_type: Optional. One between infographic, table, plot, rich-text.
    :type element_type: str | None
    """
    page_element: Element | None
    title: str | None
    element_type: Literal['infographic', 'table', 'plot', 'rich-text', 'plotly'] | None
    card_title: str | None
    @property
    def element_id(self) -> str | None: ...
    @property
    def card_id(self) -> str | None: ...
    model_config: Incomplete
    def model_post_init(self, /, __context): ...

class ChatSourceCard(BaseModel):
    title: str
    data: list[ChatSource]
    def validate_source(self, chat_context: RawChatContext): ...
    def to_dict(self): ...

class AvailableEvents(Enum):
    MESSAGE: str
    CHAT_END: str
    STATE_UPDATE: str
    PAGE_UPDATE: str
    PAGE_REFRESH: str
    UPDATE_THINKING: str
    POST_PROCESSING: str
    EXCEPTION: str

class StreamMessage(BaseModel):
    """Event for a single message token in the stream."""
    t: Literal[AvailableEvents.MESSAGE]
    d: str

class StreamSourceInformation(BaseModel):
    """Event for the final, post-processed response."""
    t: Literal[AvailableEvents.POST_PROCESSING]
    d: list[ChatSourceCard]

class StreamPageRefresh(BaseModel):
    """Event to signal a trigger to refresh the current page"""
    t: Literal[AvailableEvents.PAGE_REFRESH]
    d: Literal['']

class StreamChatEnd(BaseModel):
    """Event to signal the end of the chat stream."""
    t: Literal[AvailableEvents.CHAT_END]
    d: Literal['']

class DashboardFilter(BaseModel):
    element_id: str
    selected: str | list | dict | None
    @computed_field
    @property
    def element_type(self) -> str: ...

class StreamMessageState(BaseModel):
    t: Literal[AvailableEvents.STATE_UPDATE]
    d: dict

class ActionPageUpdate(BaseModel):
    card_id: str
    step_name: str
    filters: list[DashboardFilter] | None

class StreamActionPageUpdate(BaseModel):
    """Trigger the frontend to perform a Page Update"""
    t: Literal[AvailableEvents.PAGE_UPDATE]
    d: ActionPageUpdate

class StreamThinking(BaseModel):
    """Event to signal the end of the chat stream."""
    t: Literal[AvailableEvents.UPDATE_THINKING]
    d: str

class StreamExecutingTool(BaseModel):
    """Event to signal the end of the chat stream."""
    t: Literal['tool']
    d: str

class StreamWaitingForInput(BaseModel):
    """Event to signal the end of the chat stream."""
    t: Literal['waiting']
    d: Literal['']

class StreamException(BaseModel):
    t: Literal[AvailableEvents.EXCEPTION]
    d: str
StreamEvent = StreamMessage | StreamSourceInformation | StreamChatEnd | StreamActionPageUpdate | StreamThinking | StreamExecutingTool | StreamWaitingForInput | StreamException | StreamMessageState
