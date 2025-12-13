from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement

class DataSource(InputElement):
    '''A Data Source Input Element. 

    :param title: The title of the  element, defaults to \'\'.
    :param options: The type of data input (s3/sql/csv/xlsx).
    :param value: The file name/pointer to the data source.
    :param description: The element\'s description, defaults to \'\'.
    :param show_title: Whether to show the title on the page when rendered, defaults to True.
    :param show_description: Whether to show the description to the page when rendered, defaults to True.
    :param required: Whether a file needs to be submitted for the step to continue, defaults to True.
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param reference_id: A user-defined reference ID for the unique identification of DataSource element within the
                        Page, defaults to \'\'.


    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import DataSource
           . . .
           # Example usage
           class DataUploadStep(Step):
            def run(self, flow_metadata):
                . . .
                data_source = DataSource(
                    title="Upload data here!",
                    options=["csv"],
                    description="Example datasource usage",
                    required=True,
                )
                data_card = Card(title="Data Upload Card", content=[data_source])

    The above DataSource example will be displayed as: 

       .. image:: ../images/data_source_ex.png
          :align: center
    '''
    @validate_types
    def __init__(self, title: str = '', options: list[str] | None = None, value: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '', reference_id: str | None = '') -> None: ...
    def get_value(self) -> str:
        """Get the value of an element. If the user has interacted with the value, the default
           will be updated.
        """
