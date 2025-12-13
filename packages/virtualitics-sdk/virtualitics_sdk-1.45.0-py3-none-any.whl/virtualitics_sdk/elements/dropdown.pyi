from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from typing import Callable
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback

class Dropdown(InputElement):
    '''A Dropdown Input element.

    :param options: The options in the dropdown menu.
    :param selected: The option the user selected, defaults to [].
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param multiselect: whether the user can select multiple values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param required: whether a selection needs to be submitted for the step to continue, defaults to True
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param max_selections: The maximum number of selections that can be made at one time, no limit set by default. This value must be greater than zero.
    :param page_update: Updater function. Allows for handling dynamic page update on a page
                        Takes a StoreInterface and optionally client runners as arguments, defaults to None.
    :param reference_id: A user-defined reference ID for the unique identification of Dropdown element within the
                         Page, defaults to \'\'.

    **EXAMPLE**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import Dropdown
           . . .
           # Example usage
           class ExStep(Step):
             def run(self, flow_metadata):
               . . .
               dropdown_options = [\'a\', \'b\', \'c\']
               single_selection_dropdown = Dropdown(options=dropdown_options, 
                                                    multiselect=False, 
                                                    title="Single Selection Dropdown", 
                                                    selected=[\'a\'])
               multiple_selection_dropdown = Dropdown(options=dropdown_options, 
                                                      multiselect=True, 
                                                      title="Multiple Selection Dropdown", 
                                                      selected=[\'a\', \'b\'])
               
    The above single and multi Dropdown examples will be displayed as: 

       .. image:: ../images/dropdown_ex.png
          :align: center

    How to use page_update

        .. code-block:: python
            # Imports
            from virtualitics_sdk import Dropdown
            . . .
            . . .

            # Example page update function
            def updater(store_interface: StoreInterface):
                current_page = store_interface.get_page()
                updated_example_element = modify(example_element) # modify element(s) in the card
                current_page.replace_content_in_section(
                    elems=[updated_example_element], section_title="Ex Section", card_title="Example Card"
                )
                store_interface.update_page(current_page)

            # Example usage of page updater
            class ExStep(Step):
                def run(self, flow_metadata):
                    store_interface = StoreInterface(**flow_metadata)
                    page = store_interface.get_page()
                    . . .
                    dropdown_element = Dropdown(
                        ["yes", "no"],
                        label="Answer",
                        title="updatable",
                        placeholder="Select One",
                        page_update=updater
                    )

                    card = Card(title="Example Card",
                                content=[dropdown_element, example_element],
                    page.add_card_to_section(card, "Ex Section")
    '''
    dropdown_map: Incomplete
    required: Incomplete
    @validate_types
    def __init__(self, options: list[str | int | float] | dict[str, str | int | float], selected: list[str | int | float] | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, multiselect: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '', max_selections: int | None = None, page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
    def get_value(self) -> str | list[str]: ...
    def update_from_input_parameters(self) -> None: ...

class SingleDropdown(Dropdown):
    '''A  Single Dropdown Input element.

    :param options: The options in the dropdown menu.
    :param selected: The option the user selected, defaults to None.
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param required: whether a selection needs to be submitted for the step to continue, defaults to True
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param page_update: Updater function. Allows for handling dynamic page update on a page
                        Takes a StoreInterface and optionally client runners as arguments, defaults to None.    
    :param reference_id: A user-defined reference ID for the unique identification of SingleDropdown element within the
                         Page, defaults to \'\'.

    **EXAMPLE**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import SingleDropdown
           . . .
           # Example usage
           class ExStep(Step):
             def run(self, flow_metadata):
               . . .
               dropdown_options = [\'a\', \'b\', \'c\']
               single_selection_dropdown = SingleDropdown(options=dropdown_options,
                                                                     title="Single Selection Dropdown",
                                                                     selected=\'a\')

    '''
    def __init__(self, options: list[str | int | float] | dict[str, str | int | float], selected: int | float | str | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '', page_update: Callable | None = None, reference_id: str | None = '') -> None: ...

class MultiDropdown(Dropdown):
    '''A Multi Dropdown Input element.

    :param options: The options in the dropdown menu.
    :param selected: The option the user selected, defaults to [].
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param required: whether a selection needs to be submitted for the step to continue, defaults to True
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param max_selections: The maximum number of selections that can be made at one time, no limit set by default. This value must be greater than zero.
    :param page_update: Updater function. Allows for handling dynamic page update on a page
                        Takes a StoreInterface and optionally client runners as arguments, defaults to None.
    :param reference_id: A user-defined reference ID for the unique identification of MultiDropdown element within the
                         Page, defaults to \'\'.

    **EXAMPLE**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import MultiDropdown
           . . .
           # Example usage
           class ExStep(Step):
             def run(self, flow_metadata):
               . . .
               dropdown_options = [\'a\', \'b\', \'c\']
               multiple_selection_dropdown = MultiDropdown(options=dropdown_options,
                                                                   title="Multiple Selection Dropdown",
                                                                   selected=[\'a\', \'b\'])

    How to use page_update

        .. code-block:: python
            # Imports
            from virtualitics_sdk import MultiDropdown
            . . .
            . . .

            # Example page update function
            def updater(store_interface: StoreInterface):
                current_page = store_interface.get_page()
                updated_example_element = modify(example_element) # modify element(s) in the card
                current_page.replace_content_in_section(
                    elems=[updated_example_element], section_title="Ex Section", card_title="Example Card"
                )
                store_interface.update_page(current_page)

            # Example usage of page updater
            class ExStep(Step):
                def run(self, flow_metadata):
                    store_interface = StoreInterface(**flow_metadata)
                    page = store_interface.get_page()
                    . . .
                    dropdown_element = MultiDropdown(
                        ["yes", "no"],
                        label="Answer",
                        title="updatable",
                        placeholder="Select One or more",
                        page_update=updater
                    )

                    card = Card(title="Example Card",
                                content=[dropdown_element, example_element],
                    page.add_card_to_section(card, "Ex Section")
    '''
    def __init__(self, options: list[str | int | float] | dict[str, str | int | float], selected: list[str | int | float] | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '', max_selections: int | None = None, page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
