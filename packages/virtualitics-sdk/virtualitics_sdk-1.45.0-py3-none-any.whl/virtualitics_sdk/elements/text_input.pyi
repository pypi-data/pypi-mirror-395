from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback

class TextInput(InputElement):
    '''A Text Input element.
    
    :param value: The inputted text, defaults to \'\'.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param required: whether an input needs to be made for the step to continue, defaults to True
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the text input shown on first view of the input. Defaults to \'\'.
    :param page_update: Updater function. Allows for handling dynamic page update on a page.
                        Takes a StoreInterface and optionally client runners as arguments.
                        This update is triggered when the user blurs the input or presses the Enter key.
                        Defaults to None (no update function).
    :param required: If true, mark the field as required to require user input before the step may continue. Defaults to false.
    :param reference_id: A user-defined reference ID for the unique identification of TextInput element within the Page, defaults to \'\'.

    **EXAMPLE:**

       .. code-block:: python
           
           # Imports 
           from virtualitics_sdk import TextInput
           . . . 
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               text_input = TextInput("Initial values can be set", 
                                      title="Text Input", 
                                      label="Some Text",
                                      description="Of course we also 
                                                   allow _open ended_ text 
                                                   input such as this.",
                                                   placeholder=\'Type Something\')

    The above TextInput will be displayed as: 
               
       .. image:: ../images/text_input_ex.png
          :align: center

    How to use page_update

        .. code-block:: python
            # Imports
            from virtualitics_sdk import TextInput, StoreInterface, Card, Step
            . . .
            . . .

            # Example page update function
            def textinput_updater(store_interface: StoreInterface):
                page = store_interface.get_page()
                text_element = page.get_element_by_title(\'My Updatable Text Input\')
                new_value = store_interface.get_element_value(
                    store_interface.step_name, "My Updatable Text Input"
                )
                text_element.description = f\'You updated the text field! New value: {new_value}\'
                store_interface.update_page(page)

            # Example usage of page updater
            class ExStep(Step):
                def run(self, flow_metadata):
                    store_interface = StoreInterface(**flow_metadata)
                    page = store_interface.get_page()
                    . . .
                    text_input = TextInput(
                        "Initial value",
                        title="My Updatable Text Input",
                        description="This text input is updatable.",
                        page_update=textinput_updater
                    )

                    card = Card(title="Example Card", content=[text_input])
                    page.add_card_to_section(card, "Ex Section")

    '''
    required: Incomplete
    @validate_types
    def __init__(self, value: str = '', description: str = '', title: str = '', show_title: bool = True, show_description: bool = True, required: bool = False, label: str = '', placeholder: str = '', page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
    def get_value(self) -> str: ...
