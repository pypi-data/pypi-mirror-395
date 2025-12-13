from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement
from virtualitics_sdk.types import PageUpdateCallback as PageUpdateCallback

class NumericRange(InputElement):
    '''A Numeric Range Input Element.

    :meta private:
    :param min_range: The minimum value for the range.
    :param max_range: The maximum value for the range.
    :param min_selection: The minimum selected value. Defaults to min_range value, defaults to None.
    :param max_selection: The maximum selected value. Defaults to max_range value, defaults to None.
                          For single sided sliders, this is the value to change to set defaults.
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param single: whether this range element is for a single sided slider, defaults to False.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param step_size: The size of default intervals between the min and max, defaults to None to automatically determine step size.
    :param page_update: A callable that will be executed to update the page when the value of this element changes. The callable should not take any arguments.
    :param reference_id: A user-defined reference ID for the unique identification of NumericRange element within the
                         Page, defaults to \'\'.

    **EXAMPLE:**
    
       .. code-block:: python

           # Imports
           from virtualitics_sdk import NumericRange
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . .
               num_range = NumericRange(0,
                                        50,
                                        max_selection=10,
                                        single=True,
                                        label="Slider Value",
                                        title="Single Numeric Range",
                                        description="This is a single sided slider.",
                                        placeholder=\'Type a Number\', step_size=10)
               
    The above NumericRange will be displayed as:

       .. image:: ../images/numeric_range_ex.png
          :align: center
          :scale: 75%

    **EXAMPLE with page_update:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import NumericRange, Text
           . . .
           # Example usage
           class ExampleStep(Step):
             def __init__(self):
                 self.text_display = Text("Current value: 10")

             def update_text(self):
                 # This function will be called when the slider value changes
                 new_value = self.num_range.get_value()
                 self.text_display.content = f"Current value: {new_value}"

             def run(self, flow_metadata):
               self.num_range = NumericRange(0, 50, max_selection=10, single=True,
                                             title="Interactive Slider",
                                             page_update=self.update_text)
               return [self.num_range, self.text_display]
    '''
    single: Incomplete
    @validate_types
    def __init__(self, min_range: int | float, max_range: int | float, min_selection: int | float | None = None, max_selection: int | float | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', single: bool = False, show_title: bool = True, show_description: bool = True, label: str = '', placeholder: str = '', step_size: float | int | None = None, page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
    def get_value(self):
        """Get the value of an element. If the user has interacted with the value, the default
        will be updated.
        """

class NumericSlider(NumericRange):
    '''A Numeric Slider Input Element.

    :param min_range: The minimum value for the range.
    :param max_range: The maximum value for the range.
    :param selected: The value to change to set defaults, defaults to None.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param step_size: The size of default intervals between the min and max, defaults to None to automatically determine step size.
    :param page_update: A callable that will be executed to update the page when the value of this element changes. The callable should not take any arguments.
    :param reference_id: A user-defined reference ID for the unique identification of NumericSlider element within the
                         Page, defaults to \'\'.

    **EXAMPLE:**

        .. code-block:: python

            # Imports
            from virtualitics_sdk import NumericSlider
            . . .
            # Example usage
            class ExampleStep(Step):
                def run(self, flow_metadata):
                    . . .
                    num_slider = NumericSlider(min_range=0,
                                                max_range=50,
                                                selected=10,
                                                title="Numeric Slider",
                                                description="This is a numeric slider.",
                                            )

    **EXAMPLE with page_update:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import NumericSlider, Text
           . . .
           # Example usage
           class ExampleStep(Step):
             def __init__(self):
                 self.text_display = Text("Current value: 10")

             def update_text(self):
                 # This function will be called when the slider value changes
                 new_value = self.num_slider.get_value()
                 self.text_display.content = f"Current value: {new_value}"

             def run(self, flow_metadata):
               self.num_slider = NumericSlider(0, 50, selected=10,
                                               title="Interactive Slider",
                                               page_update=self.update_text)
               return [self.num_slider, self.text_display]
    '''
    def __init__(self, min_range: int | float, max_range: int | float, selected: int | float = None, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, step_size: float | int | None = None, page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...

class NumericRangeSlider(NumericRange):
    '''
    A Numeric Range Slider Input Element.

    :param min_range: The minimum value for the range.
    :param max_range: The maximum value for the range.
    :param min_selection: The minimum selected value. Defaults to min_range value, defaults to None.
    :param max_selection: The maximum selected value. Defaults to max_range value, defaults to None.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param step_size: The size of default intervals between the min and max, defaults to None to automatically determine step size.
    :param page_update: A callable that will be executed to update the page when the value of this element changes. The callable should not take any arguments.
    :param reference_id: A user-defined reference ID for the unique identification of NumericRangeSlider element within the
                         Page, defaults to \'\'.

    **EXAMPLE:**

        .. code-block:: python

            # Imports
            from virtualitics_sdk import NumericRangeSlider
            .  .  .
            # Example usage
            class ExampleStep(Step):
                def run(self, flow_metadata):
                    .  .  .
                    num_range_slider = NumericRangeSlider(
                                            min_range=-2,
                                            max_range=17,
                                            min_selection=0,
                                            max_selection=15,
                                            title="Numeric Range Slider",
                                            description="This is a numeric range slider between -2 and 17",
                                        )

    **EXAMPLE with page_update:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import NumericRangeSlider, Text
           . . .
           # Example usage
           class ExampleStep(Step):
             def __init__(self):
                 self.text_display = Text("Current range: 5 to 25")

             def update_text(self):
                 # This function will be called when the slider value changes
                 new_range = self.num_range_slider.get_value()
                 min_val = new_range[\'min\']
                 max_val = new_range[\'max\']
                 self.text_display.content = f"Current range: {min_val} to {max_val}"

             def run(self, flow_metadata):
               self.num_range_slider = NumericRangeSlider(0, 50, min_selection=5, max_selection=25,
                                                          title="Interactive Range Slider",
                                                          page_update=self.update_text)
               return [self.num_range_slider, self.text_display]
    '''
    def __init__(self, min_range: int | float, max_range: int | float, min_selection: int | float | None = None, max_selection: int | float | None = None, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, step_size: float | int | None = None, page_update: PageUpdateCallback | None = None, reference_id: str | None = '') -> None: ...
