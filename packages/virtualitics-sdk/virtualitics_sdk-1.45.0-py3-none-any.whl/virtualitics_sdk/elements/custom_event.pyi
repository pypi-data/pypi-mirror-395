from _typeshed import Incomplete
from enum import Enum
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.app.flow_metadata import FlowMetadata as FlowMetadata
from virtualitics_sdk.assets.asset import Asset as Asset
from virtualitics_sdk.elements.element import ElementHorizontalPosition as ElementHorizontalPosition, ElementType as ElementType, ElementVerticalPosition as ElementVerticalPosition, InputElement as InputElement
from virtualitics_sdk.icons import ALL_ICONS as ALL_ICONS

class CustomEventType(Enum):
    STANDARD: str
    ASSET_DOWNLOAD: str

class CustomEventPosition(Enum):
    """
    This is deprecated, use ElementHorizontalPosition
    """
    LEFT: str
    CENTER: str
    RIGHT: str

class CustomEvent(InputElement):
    '''Creates a custom event element that calls the passed in function using flow_metadata when clicked.

    :param title: The title of the custom event element, used as the identifier for the element.
    :param confirmation_text: A description to go with this element on the page, defaults to None.
    :param label: The label displayed on the button, defaults to None.
    :param horizontal_position: The horizontal position the event button should be placed, defaults to ElementHorizontalPosition.LEFT
    :param vertical_position: The vertical position the event button should be placed, defaults to ElementVerticalPosition.TOP
    :param icon: The icon displayed next to the button label. Must be one of the available Google icons which be viewed at :class:`~virtualitics_sdk.icons.fonts`. Defaults to \'\'.
    :param show_confirmation: Whether or not to display a confirmation modal after clicking the button, defaults to True
    :param reference_id: A user-defined reference ID for the unique identification of custom event element within the Page, defaults to \'\'.

    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import CustomEvent
           . . .
           # Example usage
           # This creates a custom event for us to place in the step defined below
           class SimpleCustomEvent(CustomEvent):
              def __init__(self):
                 super().__init__(title="Kick-off", confirmation_text="")
               def callback(self, flow_metadata) -> Union[str, dict]:
                 return "Done!"
           class ExampleStep(Step):
               def run(self, flow_metadata):
                . . .
                event = SimpleCustomEvent()
                info = Infographic("", "", [], [recommendation], event=event)
                return info

    The above CustomEvent will be displayed as:

       .. image:: ../images/custom_event_ex.png
          :align: center
          :scale: 25%
    '''
    @validate_types
    def __init__(self, title: str, confirmation_text: str = None, label: str = None, show_confirmation: bool = True, icon: str = '', open_new_tab: bool = False, vertical_position: ElementVerticalPosition = ..., horizontal_position: ElementHorizontalPosition = ..., reference_id: str | None = '', **kwargs) -> None: ...
    @validate_types
    def callback(self, flow_metadata: FlowMetadata, **step_clients: dict) -> str | dict: ...
    def get_value(self) -> None:
        """This function does nothing for Custom Events. Although they are input elements, getting their
        value will return None

        :return: None
        """

class AssetDownloadCustomEvent(CustomEvent):
    '''
    Creates a custom event that generates a download link to an Asset\'s data/object. The download link will return the
    bytes of the object if it is an instance of bytes, a text file if it is an instance of str or the dill pickled bytes
    of the python object.

    Adds some additional required parameters to the constructor.

    :param title: The title of the custom event element, used as the identifier for the element.
    :param asset: an Asset object with reference of the data/object to download.
    :param extension: A file extension of the resulting downloaded file.
    :param label: The label displayed on the button, defaults to None.
    :param mime_type: Force the mimetype of the downloaded file (this determines how the client\'s browser
            encodes or writes the file being download.
    :param reference_id: A user-defined reference ID for the unique identification of custom event element within the Page, defaults to \'\'.

    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import AssetDownloadCustomEvent
           . . .
           # Example usage
           class DataShow(Step):
            def run(self, flow_metadata):
                . . .
                acc = Model(label="linear-svc", model=LinearSVC().fit(X, y), name="Example")
                event = AssetDownloadCustomEvent("Download Linear SVC", acc, "pkl")

    The above AssetDownloadCustomEvent usage will be displayed as:

       .. image:: ../images/asset_ce_ex.png
          :align: center
          :scale: 50%
    '''
    is_asset_download: bool
    asset_download_kwargs: Incomplete
    @validate_types
    def __init__(self, title: str, asset: Asset, extension: str, label: str = None, mime_type: str | None = None, reference_id: str | None = '') -> None: ...
    @validate_types
    def callback(self, flow_metadata: FlowMetadata, **step_clients) -> str | dict: ...

class TriggerFlowCustomEvent(CustomEvent):
    '''
    Creates a custom event that triggers another app with optional pre-supplied input parameters.
    Then wait for the app to stop and return a redirect url to the last started step.

    :param title: The title of the custom event element.
    :param app_name: The name of the App to be triggered
    :param confirmation_text: A description to go with this element on the page, defaults to None.
    :param label: The label displayed on the button, defaults to None.
    :param input_parameters: an optional dictionary describing input parameters to be passed to the triggered app
    :param timeout: timeout in seconds, the amount of time to wait for the triggered app to stop [default = 30]
    :param horizontal_position: The horizontal position the event button should be placed, defaults to ElementHorizontalPosition.LEFT
    :param vertical_position: The vertical position the event button should be placed, defaults to ElementVerticalPosition.TOP
    param reference_id: A user-defined reference ID for the unique identification of custom event element within the Page, defaults to \'\'.
    :param kwargs:

    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import TriggerFlowCustomEvent
           . . .
           # Example usage
           class DataUpload(Step):
             def run(self, flow_metadata):
                . . .
                flow_input_parameters = {"steps": {
                    "DataUpload": {
                        "Dropdown One": {"value": "A",
                                         "description": "",
                                         "card_title":
                                         "User Input Card"},
                        "Dropdown Two": {"value": "B",
                                         "card_title":
                                         "User Input Card"}}}}
                trigger = TriggerFlowCustomEvent(title="Trigger a Flow",
                                                confirmation_text="",
                                                app_name="TriggerFlowTest",
                                                input_parameters=flow_input_parameters)

    The above TriggerFlowCustomEvent will be displayed as:

       .. image:: ../images/trigger_ce_ex.png
          :align: center
          :scale: 25%
    '''
    flow_name: Incomplete
    input_parameters: Incomplete
    timeout: Incomplete
    @validate_types
    def __init__(self, title: str, app_name: str, confirmation_text: str = None, label: str = None, input_parameters: dict | None = None, timeout: int = 30, horizontal_position: ElementHorizontalPosition = ..., vertical_position: ElementVerticalPosition = ..., reference_id: str | None = '', **kwargs) -> None: ...
    @validate_types
    async def callback(self, flow_metadata: FlowMetadata, **step_clients) -> str | dict: ...
