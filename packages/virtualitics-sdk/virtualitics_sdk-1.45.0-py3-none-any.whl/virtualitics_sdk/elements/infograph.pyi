from _typeshed import Incomplete
from enum import Enum
from predict_backend.validation.type_validation import validate_types
from typing import Iterator
from virtualitics_sdk import DrilldownCallback as DrilldownCallback
from virtualitics_sdk.elements.custom_event import CustomEvent as CustomEvent
from virtualitics_sdk.elements.element import Element as Element, ElementHorizontalPosition as ElementHorizontalPosition, ElementOverflowBehavior as ElementOverflowBehavior, ElementType as ElementType, ElementVerticalPosition as ElementVerticalPosition
from virtualitics_sdk.exceptions import PredictException as PredictException
from virtualitics_sdk.icons import ALL_ICONS as ALL_ICONS
from virtualitics_sdk.types import CallbackType as CallbackType, PageUpdateCallback as PageUpdateCallback, StandardEventCallback as StandardEventCallback

class InfographicOrientation(Enum):
    ROW: str
    COLUMN: str

class InfographDataType(Enum):
    POSITIVE: str
    NEGATIVE: str
    WARNING: str
    NEUTRAL: str
    INFO: str

class InfographData(Element):
    '''The information to show in an infographic block. The InfographData element can also be used independently 
    as a way to display arbitrary data.

    :param label: The label at the top of the infographic block. Note this will be used as a title as well.
    :param main_text: The main bolded text in this infographic block.
    :param supporting_text: The supporting text underneath the main text for the infographic, defaults to \'\'.
    :param icon: An optional icon to show at the top-right of the infographic. Must be one of the available Google icons which be viewed at :class:`~virtualitics_sdk.icons.fonts`. Defaults to \'\'.
    :param infograph_type: The type of infographic to show. Sets the themes/colors for this block, defaults to InfographDataType.INFO.
    :param unit: The unit to show alongside the main text, defaults to None.
    :param display_compact: If true, each tile takes up less space than a standard Infograph tile, defaults to False.
    :param callback_type: Specifies type of callback to be called on click, defaults to None.
    :param on_click: Callback executed when the InfographData is clicked. If ``callback_type`` is ``CallbackType.STANDARD`` or
                    ``CallbackType.PAGE_UPDATE``, an async callback with the following signature must be provided:

                    .. code-block:: python
                        async def callback(store_interface: StoreInterface) -> None
                    ..
                    
                    When ``callback_type`` is ``CallbackType.DRILLDOWN``, a callback of type `DRILLDOWN` must be provided.
                    The callback is persisted and invoked by the platform at runtime. It should be a callable with the 
                    following signature.

                        .. code-block:: python

                        async def callback(
                            card: "Card",
                            input_data: dict[str, str | float | int],
                            store_interface: "DrilldownStoreInterface",
                            drilldown_type: "DrilldownType" = DrilldownType.MODAL,
                            drilldown_size: "DrilldownSize" = DrilldownSize.MEDIUM,
                        ) -> None: ..

                        **Arguments passed to the callback**

                        - ``card``: A mutable container representing the drilldown surface.
                        Add elements (e.g., ``RichText``, ``Table``, ``Chart``) with ``card.add_content([...])``.
                        You may also set layout/behavior, e.g.:
                        ``card.drilldown_type = drilldown_type.value`` and
                        ``card.drilldown_size = drilldown_size.value`` (if supported).

                        - ``input_data``: A dictionary of primitive values (``str | float | int``) derived
                        from the current context (e.g., selection, row details, or filter state). Use this
                        to parameterize the drilldown (populate text, filter tables, etc.).

                        - ``store_interface``: A state helper scoped to the drilldown.  The exact API depends on
                        ``DrilldownStoreInterface``.

                        - ``drilldown_type``: Defaults to``DrilldownType.MODAL``.

                        - ``drilldown_size``: Size hint for the drilldown surface (e.g., ``SMALL``, ``MEDIUM``,
                        ``SHEET``).

                        **Return value**

                        - The return value is **ignored**; render by mutating ``card`` (add content, set type/size).

                        **Side effects & lifecycle**

                        - The callback is serialized during :py:meth:`_save` and stored server-side.
                        At click time, the platform deserializes and executes it.

                        **Content guidelines**

                        - Add content via ``card.add_content([Element,...])``. Supported elements include
                        ``RichText``, ``Table``, and other ``virtualitics_sdk`` elements.

                        **EXAMPLE**

                        .. code-block:: python

                        from typing import Any
                        import pandas as pd
                        from virtualitics_sdk import RichText, Table
                        from virtualitics_sdk.drilldown import DrilldownType, DrilldownSize
                        from virtualitics_sdk.drilldown import DrilldownStoreInterface

                        def example_callback_small(
                            card: "Card",
                            input_data: dict[str, str | float | int],
                            store_interface: DrilldownStoreInterface,
                            drilldown_type: DrilldownType = DrilldownType.MODAL,
                            drilldown_size: DrilldownSize = DrilldownSize.SMALL,
                        ) -> None:
                            # Build tabular content
                            df = pd.DataFrame([
                                {"column_1": 1, "column_2": "A", "column_3": 100.0},
                                {"column_1": 2, "column_2": "B", "column_3": 200.0},
                                {"column_1": 3, "column_2": "C", "column_3": 300.0},
                            ])

                            # Compose content from input_data plus a table
                            content: list[Any] = [RichText(title=k, content=v) for k, v in input_data.items()]
                            content.append(Table(content=df, title="Example Table"))

                            # Render into the drilldown
                            card.add_content(content)
                            card.drilldown_type = drilldown_type.value
                        
    :param open_new_tab: If ``True``, standard events will open their link in a new tab (when applicable). Defaults to ``False``.
    :param show_confirmation: If ``True``, callbacks will display a confirmation dialog before executing their action. Defaults to ``True``.
    :param horizontal_position: Horizontal alignment of the element within its card. Defaults to ``ElementHorizontalPosition.LEFT``.
    :param vertical_position: Vertical alignment of the element within its card. Defaults to ``ElementVerticalPosition.TOP``.
    :param reference_id: A user-defined reference ID for the unique identification of InfographicData element within the
                         Page, defaults to \'\'.
    :param info_content: Description to be displayed within the element\'s info button. Use RichText/Markdown for 
                         advanced formatting.
    :param kwargs: Additional parameters:
        - For ``ASSET_DOWNLOAD`` callbacks, supply:
          - ``asset``: Object with ``id``, ``type``, ``label``, ``name``, ``time_created``.
          - ``extension``: File extension for the download.
          - ``mime_type``: MIME type for the download.
          - ``label``: Optional override for the download label (defaults to ``asset.label``).
        - ``description``: Element description (ignored if ``confirmation_text`` is provided).
    :raises ValueError: If the icon is an invalid choice.
    '''
    main_text: Incomplete
    supporting_text: Incomplete
    label: Incomplete
    icon: Incomplete
    infograph_type: Incomplete
    unit: Incomplete
    display_compact: Incomplete
    callback_type: Incomplete
    info_content: Incomplete
    @validate_types
    def __init__(self, label: str, main_text: str, supporting_text: str = '', icon: str = '', infograph_type: InfographDataType = ..., unit: str | None = None, display_compact: bool = False, callback_type: CallbackType = None, on_click: DrilldownCallback | StandardEventCallback | PageUpdateCallback | None = None, open_new_tab: bool | None = False, show_confirmation: bool | None = True, horizontal_position: ElementHorizontalPosition = ..., vertical_position: ElementVerticalPosition = ..., reference_id: str | None = '', info_content: str | None = None, **kwargs) -> None: ...
    def to_json(self): ...

class Infographic(Element):
    '''An Infographic Element. 

    :param title: The title of the infographic element.
    :param description: The description of the infographic element.
    :param data: Optional list of information blocks to show, defaults to None.
    :param recommendation: Optional list of recommendation blocks to show, defaults to None.
    :param layout: This attribute is now deprecated and has no effect on how the infographic gets rendered.
    :param show_title: Whether to show the title on the page when rendered, defaults to True.
    :param show_description: Whether to show the description to the page when rendered, defaults to True.
    :param event: The CustomEvent that can be optionally added to this Infographic, defaults to None
    :param overflow_behavior: How the platform should render the element if it is larger than the default layout space. Defaults to ElementOverflowBehavior.SCROLL
    :param reference_id: A user-defined reference ID for the unique identification of Infographic element within the
                         Page, defaults to \'\'.
    :param info_content: Description to be displayed within the element\'s info button. Use RichText/Markdown for 
                         advanced formatting.
    :raises ValueError: If no data exists in the infographic.

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import InfographData, Infographic
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               pred_failure = InfographData("Predicted Failures", 
                                            "6", 
                                            "Predicted degradation failures...",
                                            "error", 
                                            InfographDataType.NEGATIVE, 
                                            display_compact=True)
               . . . 
               # multiple other InfographData elements 
               info_w_rec = Infographic("Additional Fixed Ratio Gearboxes need to be ordered",
                                        "There is sufficient time to...",
                                        [pred_failure, avg_downtime, inventory, ship_estimate], 
                                        [recommendation])
               
    The above Infographic will be displayed as: 

       .. image:: ../images/infograph_ex.png
          :align: center
          :scale: 30%
    '''
    event: Incomplete
    overflow_behavior: Incomplete
    data: Incomplete
    recommendation: Incomplete
    info_content: Incomplete
    @validate_types
    def __init__(self, title: str = '', description: str = '', data: list[InfographData] | None = None, recommendation: list[InfographData] | None = None, layout: InfographicOrientation = ..., show_title: bool = True, show_description: bool = True, event: CustomEvent | None = None, reference_id: str | None = '', overflow_behavior: ElementOverflowBehavior | None = ..., info_content: str | None = None) -> None: ...
    def to_json(self): ...
    def extract_context(self): ...
    def get_elements(self) -> Iterator[InfographData]: ...
    def update_infograph_data(self) -> None:
        """ Regenerates the inner content for the Infographic using the linked elements. """
