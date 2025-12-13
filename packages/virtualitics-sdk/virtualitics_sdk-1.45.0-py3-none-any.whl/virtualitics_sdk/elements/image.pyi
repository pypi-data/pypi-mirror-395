from PIL.Image import Image as PILImage
from _typeshed import Incomplete
from enum import Enum
from io import BytesIO
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import Element as Element, ElementOverflowBehavior as ElementOverflowBehavior, ElementType as ElementType

class ImageSize(Enum):
    SMALL: str
    MEDIUM: str
    LARGE: str

class Image(Element):
    '''An image to show on an app. 

    :param content: The PIL image to show on an app.
    :param size: The size of the image to display, defaults to ImageSize.MEDIUM.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: Whether to show the title on the page when rendered, defaults to True.
    :param show_description: Whether to show the description to the page when rendered, defaults to True.
    :param overflow_behavior: How the platform should render the element if it is larger than the default layout space. Defaults to ElementOverflowBehavior.SCROLL    
    :param reference_id: A user-defined reference ID for the unique identification of Image element within the
                         Page, defaults to \'\'.
    :param info_content: Description to be displayed within the element\'s info button. Use RichText/Markdown for 
                         advanced formatting.
    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from io import BytesIO
           from PIL import Image as PILImage
           from virtualitics_sdk import Image
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               jpeg_content = PILImage.open(BytesIO(store_interface.get_s3_asset("ex_path/image/ex.jpg")))
               jpeg_1 = Image(content=jpeg_content, size=ImageSize.SMALL, title="This is a small image")
               jpeg_2 = Image(content=jpeg_content, size=ImageSize.MEDIUM, title="This is a medium image")
               jpeg_3 = Image(content=jpeg_content, size=ImageSize.LARGE, title="This is a large image")
    '''
    info_content: Incomplete
    @validate_types
    def __init__(self, content: PILImage | BytesIO, size: ImageSize = ..., title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, extension: str = 'jpeg', raw_image_bytes: bool = False, overflow_behavior: ElementOverflowBehavior = ..., reference_id: str | None = '', info_content: str | None = None) -> None: ...
    def to_json(self): ...
