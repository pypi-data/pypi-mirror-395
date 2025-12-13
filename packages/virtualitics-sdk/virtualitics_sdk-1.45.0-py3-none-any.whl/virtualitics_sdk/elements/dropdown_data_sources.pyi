from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.dropdown import Dropdown as Dropdown
from virtualitics_sdk.utils.types import ConnectionType as ConnectionType

class DataSourceDropdown(Dropdown):
    """
    Used to configure data source drop down options that have been set up in the Connections tab.
   
    :param user_id: the user_id of the owner of the connections, usually done via StoreInterface.user.
    :param options: a list of ConnectionTypes, for example ConnectionType.mssql.
    :param selected: used if you want a default selection.
    :param include_nulls_visible: whether null values will be visible.
    :param include_nulls_value: whether to include null values.
    :param title: the title of the drop-down element.
    :param description: the description of the drop-down element.
    :param show_title: whether to show the title.
    :param show_description: whether to show the description.
    :param required: whether selecting an item from the dropdown is required to proceed.
    :param label: the label of the element.
    :param placeholder: the placeholder of the element.

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import DataSourceDropdown
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               api_key_selection = DataSourceDropdown(user_id=store_interface.user,
                                                      options=[ConnectionType.s3, ConnectionType.other],
                                                      title='Select API Credential')
               
    The above DataSourceDropdown example will be displayed as: 

       .. image:: ../images/dropdown_data_ex.png
          :align: center
    """
    user_id: Incomplete
    required: Incomplete
    @validate_types
    def __init__(self, user_id: str, options: list[ConnectionType], selected: list[str] | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '') -> None: ...
    @staticmethod
    def conn2dropdown_str(filter_options, user_id: str): ...
    @staticmethod
    @validate_types
    def dropdown_str2conn(user_id: str, connection_str: str): ...
    def get_value(self) -> str | dict: ...
