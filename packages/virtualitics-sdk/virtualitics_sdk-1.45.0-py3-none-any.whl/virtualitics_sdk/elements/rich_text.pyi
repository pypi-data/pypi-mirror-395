from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from typing import Any
from virtualitics_sdk import DrilldownCallback as DrilldownCallback
from virtualitics_sdk.elements.element import Element as Element, ElementOverflowBehavior as ElementOverflowBehavior, ElementType as ElementType
from virtualitics_sdk.types import CallbackType as CallbackType, PageUpdateCallback as PageUpdateCallback, StandardEventCallback as StandardEventCallback

class RichText(Element):
    '''A Rich Text Element.

    :param content: The value inside the rich text element
    :param border: whether to surround the text with a border, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param overflow_behavior: how the platform should handle richtext content that renders outside the size of the
                              parent element.
    :param reference_id: A user-defined reference ID for the unique identification of RichText element within the
                        Page, defaults to \'\'.
    :param info_content: Description to be displayed within the element\'s info button. Use RichText/Markdown for
                         advanced formatting.
    :param on_click: Optional callback executed when clickable regions (marked with data-virt-clickable) are clicked.
                     Can be a DrilldownCallback, StandardEventCallback, or PageUpdateCallback. The callback will
                     receive parameters from the data-params attribute of the clicked element.

    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import RichText
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . .
               new_rich_text_1 = RichText("""
                    The usual [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
                    does not cover some of the more advanced Markdown tricks, but here
                    is one. You can combine verbatim HTML with your Markdown.
                    This is particularly useful for tables.
                    Notice that with **empty separating lines** we can use Markdown inside HTML:

                    <table>
                    <tr>
                    <th>Json 1</th>
                    <th>Markdown</th>
                    </tr>
                    <tr>
                    <td>
                    <pre>
                    "id": 1,
                    "username": "joe",
                    "email": "joe@example.com",
                    "order_id": "3544fc0"
                    </pre>
                    </td>
                    <td>


                    "id": 5,
                    "username": "mary",
                    "email": "mary@example.com",
                    "order_id": "f7177da"
                    </td>
                    </tr>
                    </table>""", border=False)

    The above RichText will be displayed as:

       .. image:: ../images/rich_text_ex.png
          :align: center
          :scale: 35%

    '''
    overflow_behavior: Incomplete
    on_click: Incomplete
    info_content: Incomplete
    @validate_types
    def __init__(self, content: str, border: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, overflow_behavior: ElementOverflowBehavior = ..., reference_id: str | None = '', info_content: str | None = None, on_click: DrilldownCallback | StandardEventCallback | PageUpdateCallback | None = None, callback_type: CallbackType | None = None) -> None: ...
    def to_json(self): ...

class RichTextClickable:
    '''Helper to generate clickable regions in RichText content.

    This class provides methods to wrap content in clickable elements that will
    trigger callbacks when clicked. The callbacks are handled by the /controller/click
    endpoint and can pass custom parameters.

    **EXAMPLE:**

    .. code-block:: python

        from virtualitics_sdk import RichText, RichTextClickable

        # Simple text link
        content = f\'\'\'
        Click {RichTextClickable.wrap("here", {"action": "filter", "value": "active"})}
        to filter the data.
        \'\'\'

        # Wrap an image
        content = f\'\'\'
        {
            RichTextClickable.wrap(
                \'<img src="chart.png" alt="Chart" style="width: 200px;" />\',
                {"action": "expand", "chart_id": 123},
                element="div",
            )
        }
        \'\'\'

        rich_text = RichText(content)
    '''
    @staticmethod
    def wrap(content: str, params: dict[str, Any], element: str = 'span', style: str | None = None, css_class: str | None = None) -> str:
        '''Wrap content in a clickable region.

        :param content: HTML/text content to make clickable. Can contain any valid HTML.
        :param params: Dictionary of parameters to pass to the click callback.
                       These will be available in the callback function.
        :param element: HTML element to use as wrapper (span, div, button, etc.).
                        Defaults to "span" for inline content.
        :param style: Optional inline CSS styles to apply to the wrapper element.
        :param css_class: Optional CSS class name(s) to apply to the wrapper element.

        :returns: HTML string with the content wrapped in a clickable element.

        **EXAMPLE:**

        .. code-block:: python

            # Basic usage
            RichTextClickable.wrap("Click me", {"page": 2})
            # Returns: \'<span data-virt-clickable data-params="{...}">Click me</span>\'

            # With styling
            RichTextClickable.wrap(
                "Styled button",
                {"action": "submit"},
                element="div",
                style="padding: 10px; background: blue; color: white;",
                css_class="custom-button",
            )
        '''
    @staticmethod
    def button(text: str, params: dict[str, Any], primary: bool = False) -> str:
        '''Create a styled button that triggers a callback.

        This is a convenience method that creates a button-styled clickable element.

        :param text: The button text to display.
        :param params: Dictionary of parameters to pass to the click callback.
        :param primary: If True, styles as a primary button. Otherwise secondary style.

        :returns: HTML string with a button-styled clickable element.

        **EXAMPLE:**

        .. code-block:: python

            RichTextClickable.button("Submit", {"action": "save"}, primary=True)
        '''
    @staticmethod
    def link(text: str, params: dict[str, Any], style: str | None = None) -> str:
        '''Create a link-styled clickable element.

        This is a convenience method that creates a link-styled clickable element
        without actually being an anchor tag (which would cause navigation).

        :param text: The link text to display.
        :param params: Dictionary of parameters to pass to the click callback.
        :param style: Optional additional CSS styles.

        :returns: HTML string with a link-styled clickable element.

        **EXAMPLE:**

        .. code-block:: python

            RichTextClickable.link("View details", {"item_id": 42})
        '''
