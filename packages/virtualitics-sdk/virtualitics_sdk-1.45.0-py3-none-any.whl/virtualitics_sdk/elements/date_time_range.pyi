from datetime import datetime
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback

class DateTimeRange(InputElement):
    '''A DateTimeRange Input element.

    :param min_range: The minimum date in the range.
    :param max_range: The maximum date in the range.
    :param min_selection: The mimumum selected date. Defaults to the min_range value.
    :param max_selection: The maximum selected date. Defaults to max_range value.
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param timezone: The timezone for the element, defaults to \'UTC\'.
    :param page_update: Updater function. Allows for handling dynamic page update on a page.
                        Takes a StoreInterface and optionally client runners as arguments.
                        This update is triggered when the user blurs the input and the value has changed.
                        Defaults to None (no update function).
    :param reference_id: A user-defined reference ID for the unique identification of DataSource element within the
                         Page, defaults to \'\'.
    
    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import DateTimeRange
           . . .
           # Example usage
           class LandingStep(Step):
             def run(self, flow_metadata):
               . . . 
               date_range = DateTimeRange(datetime.today().replace(year=2000),
                                          datetime.today().
                                          replace(year=2020), 
                                          title="Date Time Range", 
                                          description= "Here\'s a datetime range 
                                                        from the beginning of the 
                                                        month to now.")

    The above DateTimeRange example will be displayed as: 

       .. image:: ../images/date_time_range_ex.png
          :align: center

    How to use page_update

        .. code-block:: python

            # Imports
            from virtualitics_sdk import DateTimeRange, StoreInterface, Card, Step
            from datetime import datetime
            . . .
            . . .

            # Example page update function
            def datetime_range_updater(store_interface: StoreInterface):
                page = store_interface.get_page()
                datetime_element = page.get_element_by_title(\'My Updatable Datetime Range\')
                new_value = store_interface.get_element_value(
                    store_interface.step_name, "My Updatable Datetime Range"
                )
                datetime_element.description = f\'You updated the date range! New value: {new_value}\'
                store_interface.update_page(page)

            # Example usage of page updater
            class ExStep(Step):
                def run(self, flow_metadata):
                    store_interface = StoreInterface(**flow_metadata)
                    page = store_interface.get_page()
                    . . .
                    datetime_range = DateTimeRange(
                        min_range=datetime(2020, 1, 1),
                        max_range=datetime(2021, 1, 1),
                        title="My Updatable Datetime Range",
                        description="This datetime range is updatable.",
                        page_update=datetime_range_updater
                    )

                    card = Card(title="Example Card", content=[datetime_range])
                    page.add_card_to_section(card, "Ex Section")
    '''
    time_format: str
    @validate_types
    def __init__(self, min_range: datetime, max_range: datetime, min_selection: datetime | None = None, max_selection: datetime | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, label: str = '', placeholder: str = '', timezone: str = 'UTC', page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
    def get_value(self):
        """Get the value of an element. If the user has interacted with the value, the default
           will be updated.
        """
