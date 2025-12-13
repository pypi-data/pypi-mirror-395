from _typeshed import Incomplete
from enum import Enum
from virtualitics_sdk import DrilldownCallback as DrilldownCallback
from virtualitics_sdk.elements.element import Element as Element, ElementHorizontalPosition as ElementHorizontalPosition, ElementType as ElementType, ElementVerticalPosition as ElementVerticalPosition
from virtualitics_sdk.icons import ALL_ICONS as ALL_ICONS
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback, StandardEventCallback as StandardEventCallback

class ButtonType(Enum):
    STANDARD: str
    ASSET_DOWNLOAD: str
    DRILLDOWN: str
    PAGE_UPDATE: str

class ButtonStyle(Enum):
    PRIMARY: str
    SECONDARY: str
    GHOST: str

class ButtonColor(Enum):
    ACCENT: str
    NEUTRAL: str
    ALERT: str

class Button(Element):
    '''A configurable Button Element.

    :param title: The title of the element. Also used as the default button label if ``label`` is not provided.
    :param confirmation_text: Optional confirmation text displayed in the element description area. If provided, it overrides ``description``.
    :param label: The text displayed on the button face. Defaults to ``title`` if omitted.
    :param icon: Optional icon name. Must be a valid entry in ``virtualitics_sdk.icons.ALL_ICONS``.
    :param on_click: Callback executed when the button is clicked. If ``button_type`` is ``ButtonType.STANDARD`` or
                    ``ButtonType.PAGE_UPDATE``, an async callback with the following signature must be provided:

                    .. code-block:: python
                        async def callback(store_interface: StoreInterface) -> None
                    ..
                    
                    When when ``button_type`` is ``ButtonType.DRILLDOWN``, a callback of type `DRILLDOWN` must be provided.
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

    :param button_type: The behavior of the button. Defaults to ``ButtonType.STANDARD``.
    :param style: Visual style of the button (primary, secondary, ghost). Defaults to ``ButtonStyle.SECONDARY``.
    :param color: Color styling for the button (accent, neutral, alert). Defaults to ``ButtonColor.ACCENT``.
    :param horizontal_position: Horizontal alignment of the element within its card. Defaults to ``ElementHorizontalPosition.LEFT``.
    :param vertical_position: Vertical alignment of the element within its card. Defaults to ``ElementVerticalPosition.TOP``.
    :param tooltip: Optional tooltip shown on hover.
    :param open_new_tab: If ``True``, standard buttons will open their link in a new tab (when applicable). Defaults to ``False``.
    :param show_confirmation: If ``True``, buttons will display a confirmation dialog before executing their action. Defaults to ``True``.
    :param reference_id: A user-defined reference ID for the unique identification of Button element within the
                         Page, defaults to \'\'.
    :param kwargs: Additional parameters:
        - For ``ASSET_DOWNLOAD`` buttons, supply:
          - ``asset``: Object with ``id``, ``type``, ``label``, ``name``, ``time_created``.
          - ``extension``: File extension for the download.
          - ``mime_type``: MIME type for the download.
          - ``label``: Optional override for the download label (defaults to ``asset.label``).
        - ``description``: Element description (ignored if ``confirmation_text`` is provided).
    '''
    button_type: Incomplete
    on_click: Incomplete
    horizontal_position: Incomplete
    vertical_position: Incomplete
    def __init__(self, *, title: str, confirmation_text: str | None = None, label: str | None = None, icon: str | None = None, on_click: DrilldownCallback | StandardEventCallback | PageUpdateCallback | None = None, button_type: ButtonType | None = ..., style: ButtonStyle | None = ..., color: ButtonColor | None = ..., horizontal_position: ElementHorizontalPosition = ..., vertical_position: ElementVerticalPosition = ..., tooltip: str | None = None, open_new_tab: bool | None = False, show_confirmation: bool | None = True, reference_id: str | None = '', **kwargs) -> None: ...
    @staticmethod
    def get_asset_download_params(asset, label, extension, mime_type): ...
    def to_json(self) -> dict: ...
