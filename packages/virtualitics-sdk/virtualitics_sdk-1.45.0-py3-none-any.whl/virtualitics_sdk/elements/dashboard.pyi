import virtualitics_sdk
from _typeshed import Incomplete
from enum import Enum
from predict_backend.validation.type_validation import validate_types
from typing import Callable, Iterator, TypeAlias, TypeVar
from virtualitics_sdk.elements.element import Element as Element, ElementType as ElementType, InputElement as InputElement
from virtualitics_sdk.elements.image import Image as Image
from virtualitics_sdk.elements.infograph import Infographic as Infographic
from virtualitics_sdk.elements.plotly_plot import PlotlyPlot as PlotlyPlot
from virtualitics_sdk.elements.rich_text import RichText as RichText
from virtualitics_sdk.elements.table import Table as Table

DASHBOARD_ELEMENT: TypeAlias = PlotlyPlot | Image | Table | Infographic | RichText
DASHBOARD_TYPES: Incomplete

def valid_dashboard_element(elem_row_or_col: DASHBOARD_ELEMENT | virtualitics_sdk.elements.dashboard.Row | virtualitics_sdk.elements.dashboard.Column): ...
ListType = TypeVar('ListType')

def simplify(elements: list[ListType]) -> list[ListType]:
    """Simplifies a Dashboard representation by replacing Row/Columns with only one element and no special ratios

    :param elements: The list of elements to enter a Row or Column
    :return: A simplified list that may replace an inner row or colum with the encapsulated dashboard element
    """

class Row:
    """A Row in a :class:`~virtualitics_sdk.elements.dashboard.Dashboard`. A :class:`~virtualitics_sdk.elements.dashboard.Dashboard` is fundamentally a list of :class:`~virtualitics_sdk.elements.dashboard.Row` s.

    :param elements: A list of elements in the row. This can be any element like a :class:`~virtualitics_sdk.elements.dropdown.Dropdown`
         element or an inner :class:`~virtualitics_sdk.elements.dashboard.Column` inside of that Row.
    :param ratio: The relative widths of the elements inside the :class:`~virtualitics_sdk.elements.dashboard.Row`,
        defaults to all elements having the same width.
    :raises ValueError: If the given ratio array is not equal the number of elements.
    :raises ValueError: If all columns in that row do not have the same height.
    """
    elements: Incomplete
    ratio: Incomplete
    width: Incomplete
    height: int
    @validate_types
    def __init__(self, elements: list[Element | virtualitics_sdk.elements.dashboard.Column], ratio: list[int | float] | None = None) -> None: ...
    def to_json(self): ...

class Column:
    """A Column vertically contains elements within a :class:`~virtualitics_sdk.elements.dashboard.Row`. A column can also contain inner rows.

    :param elements: The Elements or :class:`~virtualitics_sdk.elements.dashboard.Row`s within this :class:`~virtualitics_sdk.elements.dashboard.Column`.
    :param ratio: The relative heights of all of the elements in the :class:`~virtualitics_sdk.elements.dashboard.Column`, defaults to equal heights.
    :raises ValueError: If the given ratio array is not equal the number of elements.
    :raises ValueError: If all rows in that column do not have the same width.
    """
    elements: Incomplete
    type: str
    ratio: Incomplete
    height: Incomplete
    width: int
    @validate_types
    def __init__(self, elements: list[Element | virtualitics_sdk.elements.dashboard.Row], ratio: list[int | float] | None = None) -> None: ...
    def to_json(self) -> dict: ...

class DashboardOrientation(Enum):
    ROW: str
    COLUMN: str

class Dashboard(Element):
    '''
    **NOTICE: As of version 1.23.0 the Dashboard element is depreciated. It is recommended to use**
    :class:`~virtualitics_sdk.page.card.Card` **elements in place of Dashboard elements.**
    
    A Dashboard is a way to lay out certain elements on a page. This can be done by placing those
    elements in rows or columns. Only Plots, Images, Infographics, and Tables can be put into Dashboards.

    :param content: The list or Rows or elements that makes up a dashboard. Any lone elements in this list will be put into their own row.
    :param title: The title of the dashboard, defaults to "".
    :param description: The description of the dashboard, defaults to "".
    :param orientation: (deprecated) the Dashboard\'s orientation, defaults to None.
    :param show_title: whether to show the title of the dashboard, defaults to True.
    :param show_description: Whether or now to show the description of a dashboard, defaults to True.
    :param filters: A list of input elements that can be used as input to the dashboard\'s updater function, defaults to None.
    :param updater: A function to provide dynamic updates to the dashboard which can use inputs from the dashboard filters, defaults to None.
    :raises ValueError: If the dashboard has no content.
    :raises ValueError: If all rows do not have the same width.
    '''
    filters: Incomplete
    has_updater: Incomplete
    updater: Incomplete
    updater_name: Incomplete
    @validate_types
    def __init__(self, content: list[Row | Column | DASHBOARD_ELEMENT], title: str = '', description: str = '', orientation: DashboardOrientation | None = None, show_title: bool = True, show_description: bool = True, filters: list[InputElement] | None = None, updater: Callable | None = None) -> None: ...
    def to_json(self, delta: set[str] = None) -> dict: ...
    def update_item(self, element_title: str, new_element: DASHBOARD_ELEMENT):
        """This function updates an element of the dashboard, which can be used in conjunction with
        the dashboard's `updater` function to provide dynamic page updates.

        :param element_title: The title of the element to be updated.
        :param new_element: The new element that will replace currently existing element.
        """
    def get_elements(self) -> Iterator[DASHBOARD_ELEMENT]: ...
    def get_filters(self) -> Iterator[InputElement]: ...
