import boto3
import pandas
from _typeshed import Incomplete
from io import BytesIO
from sqlalchemy.orm import DeclarativeBase as DeclarativeBase, MappedAsDataclass as MappedAsDataclass
from sqlalchemy.sql import ColumnElement as ColumnElement
from typing import TypedDict
from virtualitics_sdk.assets.asset import Asset as Asset, AssetPersistenceMethod as AssetPersistenceMethod, AssetType as AssetType
from virtualitics_sdk.assets.dataset import Dataset as Dataset
from virtualitics_sdk.assets.model import Model as Model
from virtualitics_sdk.assets.schema import Schema as Schema
from virtualitics_sdk.elements import DataSource as DataSource
from virtualitics_sdk.elements.element import Element as Element, InputElement as InputElement
from virtualitics_sdk.page.page import Page as Page
from virtualitics_sdk.utils.types import ConnectionType as ConnectionType

logger: Incomplete

class DatasetIndex(TypedDict):
    """
    Type Hint for specifying Dataset Asset Indexes in StoreInterface.save_datastore_asset
    """
    columns: list[str]
    unique: bool | None

class StoreInterface:
    '''
    The StoreInterface class is the main interface to storing and retrieving metadata.
    It provides convenience methods for storing input data, assets and flow metadata and also methods
    for retrieving previously saved data.

    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import StoreInterface
           . . .
           # Example usage
           class ExStep(Step):
             def run(self, flow_metadata):
                store_interface = StoreInterface(**flow_metadata)
                page = store_interface.get_page()
                data_source = DataSource(title="Upload data here!",
                                            options=["csv"],
                                            description="Simple data upload example",
                                            required=True,)
                data_card = Card(title="Data Upload Card", content=[data_source])
                page.add_card_to_section(data_card, "")
                store_interface.update_page(page)

    '''
    flow_id: Incomplete
    step_name: Incomplete
    is_action: Incomplete
    user: Incomplete
    flow_data: Incomplete
    app_id: Incomplete
    bucket_name: Incomplete
    s3_handler: Incomplete
    def __init__(self, flow_id: str, user: str | None = None, step_name: str | None = None, is_action: bool = False, bucket_name: str | None = None) -> None:
        """
        :meta private:
        :param flow_id:
        :param user:
        :param step_name:
        :param is_action:
        :param bucket_name:
        """
    def get_previous_step_name(self) -> str | None: ...
    @staticmethod
    def update_progress(completion: float | int, message: str, page_update: bool = False):
        """
        Update the progress of the step as it's running. It is recommended to use this when steps
        have operations that can take a long time.

        :param completion: The progress to completion (0 to 100).
        :param message: The message to show at this level of completion.
        :return: True if the progress message was sent successfully.
        """
    @staticmethod
    async def aupdate_progress(completion: float | int, message: str, page_update: bool = False):
        """
        Update the progress of the step as it's running. It is recommended to use this when steps
        have operations that can take a long time.

        :param completion: The progress to completion (0 to 100).
        :param message: The message to show at this level of completion.
        :return: True if the progress message was sent successfully.
        """
    def get_page(self, _out_link=None) -> Page:
        """
        Get the most up to date version of the page for this step.

        :param _out_link: optionally pass an existing outlink reference to prevent repeated calls to get_outlink() and
                          to improve performance

        :return: The most up to date Page for this step.
        """
    def update_page(self, page: Page):
        """
        Update a page. This is usually called from within a step to dynamically update content on
        the page as the step is running.

        :param page: The Page object containing updates.
        """
    @staticmethod
    def extract_context_from_page(page: Page): ...
    def save_output(self, data: pandas.DataFrame | pandas.Series | dict | int | float | BytesIO, name: str):
        """Save the intermediate value of some information for access in a later step

        :param data: The data to save.
        :param name: The label to use the access this data in a later step.
        :raises ValueError: If the data passed in is no pickleable.
        :raises ValueError: An invalid persistence method is used.
        """
    def has_input(self, name: str) -> bool:
        """
        Check if a step contains a link to an input

        :param name: the name to check for
        :return: does the name exist within the step's in_link
        """
    def get_input(self, name: str, step_name: str | None = None):
        """Get a previously stored input value stored with `save_output`.

        :param name: The input name.
        :param step_name: [Optional] The step name to retrieve the input data from
        :raises ValueError: If the name is not not found in the database.
        :return: The previously saved data.
        """
    def get_element_value(self, step_name: str, elem_reference_id: str = '', quiet: bool = False, **kwargs):
        """Get the value of an element the user interacted with in the Virtualitics AI Platform.

        :param step_name: The name of the step the element was in.
        :param elem_reference_id: The reference_id of the element to select.
        :param quiet: if True, return None instead of error if the element does not exist. Defaults to False.
        :param kwargs: Accepts 'elem_title' (deprecated).
        :return: The value of that element interaction. This will differ by input element type.
        """
    def get_element_by_id(self, step_name: str, elem_id: str) -> Element:
        """Get an element from any step by its auto-generated ID

        :param step_name: the step name where the element was created
        :param elem_id: the element id
        :return: an Element object
        """
    def get_element(self, step_name: str, elem_reference_id: str, quiet: bool = False) -> Element:
        """Get an element from any step by its title.

        :param step_name: the step name where the element was created
        :param elem_reference_id: the reference_id of the element to lookup
        :param quiet: if True, return None instead of error if the element does not exist. Defaults to False.
        :return:
        """
    def create_future_element(self, elem: Element, future_step_name: str):
        '''Create a link to an element that will be created in the next step.

        :param elem: Element that we want to link.
        :param future_step_name: The name of the future step in which the element will be inserted.

        **EXAMPLE:**

            .. code-block:: python

                # Imports
                from virtualitics_sdk import StoreInterface
                .  .  .

                class ExampleStep(Step):
                    def run(self, flow_metadata):
                        .  .  .
                        future_dropdown = Dropdown(
                            ["Rows", "Columns"],
                            selected=["Rows"],
                            title="Dashboard Options",
                            label="Option Selector",
                        )
                        store_interface.create_future_element(future_dropdown, future_step.name)

                        table_links = [
                            "https://www.google.com",
                            store_interface.create_element_link(future_dropdown, future_step.name)
                            ]

                        table = Table(example_dataset,
                                title="Example Table",
                                description="This is a table showing cells/text color",
                                downloadable=True,
                                links=table_links)
                        .  .  .

                class FutureSte(Step):
                    def run(self, flow_metadata):
                        .  .  .
                        dropdown = store_interface.get_element(example_step.name, "Dashboard Options")
                        .  .  .

        '''
    def create_element_link(self, element: Element, step_name: str | None = None):
        '''Create a link to any element present in the current step or in the previous ones.

        :param element: Element that we want to link.
        :param step_name: The name of the step the element was in.
        :return:

        **EXAMPLE:**

            .. code-block:: python

                # Imports
                from virtualitics_sdk import StoreInterface
                .  .  .

                class PreviousStep(Step):
                    def run(self, flow_metadata):
                        .  .  .
                        text = TextInput(title="Some Text")
                        .  .  .

                class ExampleStep(Step):
                    def run(self, flow_metadata):
                        .  .  .
                        prev_text_input = store_interface.get_element(previous_step.name, "Some Text")

                        table_links = [
                            "https://www.google.com",
                            store_interface.create_element_link(prev_text_input, previous_step.name)
                            ]

                        table = Table(example_dataset,
                                title="Example Table",
                                description="This is a table showing links",
                                downloadable=True,
                                links=table_links)
                        .  .  .

        '''
    def save_asset(self, asset: Asset, overwrite: bool = False, asset_id: str | None = None, serialization_method: AssetPersistenceMethod | None = None):
        """
        Save an Asset. This is useful for storing objects, datasets, models to be used in
        other apps or within the current flow. Assets are persisted until they are deleted (even if
        the flow they were created in is deleted)

        :param asset: The asset object to save.
        :param overwrite: bool: Overwrite the existing asset with the same label and type if it exists
        :param asset_id: str: An optional asset_id to use when overwriting
        :param serialization_method: AssetPersistenceMethod: An Optional argument to force serialization using a specific method
        """
    def get_asset(self, label: str | None = None, type: AssetType | None = None, name: str | None = None, time_created: str | None = None, asset_id: str | None = None) -> Asset:
        """
        Retrieve a saved Asset. This function returns (at most) 1 asset, use get_assets for retrieving a list of assets
        that matches the supplied argument values. This function will only return an asset that the requesting user has
        access to

        :param label: The label of the Asset, defaults to None.
        :param type: The type of asset, defaults to None.
        :param name: The name for the asset, defaults to None.
        :param time_created: The time the asset was created. This is especially optional and only necessary when you want
                             to receive an Asset by timestamp as well as other metadata, defaults to None.
        :param asset_id: The unique identifier of a specific asset, defaults to None
        :raises ValueError: If the asset label and type are both None.
        :return: The Asset object.
        """
    def get_assets(self, label: str | None = None, type: AssetType | None = None, name: str | None = None, asset_id: str | None = None) -> list[Asset]:
        """
        Retrieve multiple saved Assets. Providing any of the attributes will filter all available
        assets to retrieve only the ones which match the given label, type, name, combination.
        Providing none of these descriptors will retrieve all available assets.

        :param label: The label of the Asset, defaults to None.
        :param type: The type of asset, defaults to None.
        :param name: The name for the asset, defaults to None.
        :param asset_id: The unique identifier of a specific asset, defaults to None
        :return: List of Asset objects.
        """
    def get_asset_by_id(self, asset_id: str) -> Asset:
        """
        Retrieve a saved asset using the asset_id

        :param asset_id: The unique identifier of a specific asset.
        :return: The Asset object.
        """
    def get_model(self, label: str | None = None, name: str | None = None) -> Model:
        '''
        This is a convenience method for getting Assets that have a "Model" type

        :param label: The label of the asset, defaults to None.
        :param name: The name of the asset, defaults to None.
        :return: The Model asset.
        '''
    def get_dataset(self, label: str | None = None, name: str | None = None) -> Dataset:
        '''
        This is a convenience method for getting Assets that have a "Dataset" type

        :param label: The label of the asset, defaults to None.
        :param name: The name of the asset, defaults to None.
        :return: The Dataset asset.
        '''
    def get_schema(self, label: str | None = None, name: str | None = None) -> Schema:
        '''
        This is a convenience method for getting Assets that have a "Schema" type

        :param label: The label of the asset, defaults to None.
        :param name: The name of the asset, defaults to None.
        :return: The Schema asset.
        '''
    def get_s3_asset(self, path: str):
        """
        Retrieve an asset from a pre-specified bucket. In order to use, please initialize the store interface with
        the `bucket_name` parameter.
        TODO: this asset wont exist in the asset store, this function might need to be removed if possible

        :param path: The path to the asset in the s3 bucket.
        :return: returns the asset from s3
        """
    def update_page_from_live_card(self, section_title: str, card_id: str, **step_clients):
        """
        :meta private:
        :param section_title:
        :param card_id:
        :param step_clients:
        :return:
        """
    def get_current_step_user_input(self, data_source_reference_id: str = '', **kwargs) -> BytesIO:
        """
        Get the raw bytes that were uploaded in the current step (prior to the step action). This can be useful for
        doing data validation on the uploaded data in a dynamic page update function. When uploading data using the
        DataSource element the data is not converted into a dataframe until the step action is run (Next button) which
        also puts the data on the subsequent steps in-link. This means that you cannot access the uploaded object using
        the common methods which retrieve data from the in-link

        :param data_source_reference_id: the eference_id of the DataSource element
        :return: a BytesIO object of the data that was uploaded
        """
    def db_to_pandas(self, query: str, conn_name: str, connection_owner: str | None = None, **kwargs):
        """
        **NOTICE: As of version 1.23.0 this function is depreciated**

        Given a SQL query and a connection name of a connection stored in the connection store execute the query
        against the defined data store connection and return the result set as a pandas data frame

        :param query: The SQL query to execute against the supplied data store
        :param conn_name: The connection name where database credentials, host, etc will be retrieved from the connection
                          store
        :param connection_owner: (optional) The owner of the connection being retrieved, this defaults to the current
                                 user
        :param kwargs: additional keyword arguments, for databricks connections http_path can be supplied here to
                       override the default http_path stored in the connection store
        :return: A pandas data frame
        """
    def pandas_to_db(self, _df: pandas.DataFrame, table: str, conn_name: str, connection_owner: str | None = None, if_exists: str = 'fail', **kwargs):
        """
        **NOTICE: As of version 1.23.0 this function is depreciated**

        Write the contents of a dataframe to the supplied data store table. Retrieve DB connection details by supplying
        the connection name and the connection owner (optional)

        :param _df: The pandas dataframe to be written
        :param table: The destination table where data will be written
        :param conn_name: The connection name where database credentials, host, etc will be retrieved from the connection
                          store
        :param connection_owner: (optional) The owner of the connection being retrieved, this defaults to the current
                                 user
        :param if_exists: What to do if the table already exists: 'fail', 'replace', 'append'
        :param kwargs: additional keyword arguments, for databricks connections http_path can be supplied here to
                       override the default http_path stored in the connection store
        :return:
        """
    def get_flow_status(self): ...
    def list_fixture_data(self, prefix: str | None = None) -> list[str]:
        """
        List all of the objects stored within the deployment's fixture path in s3://{meta-data-bucket}/fixture/{prefix}

        :param prefix: Optional prefix to filter objects

        :return: list of s3 keys
        """
    @staticmethod
    def str_2_connection_type(list_connection_type: list[str]) -> list[ConnectionType]:
        """
        Converts a list of strings representing the connection type to a list of ConnectionType

        :param list_connection_type: list of strings representing the connection type

        :return: list of ConnectionType
        """
    def get_raw_data_source_data(self, step_name: str | None = None, element_id: str | None = None, elem_reference_id: str | None = None) -> BytesIO: ...
    def get_boto3_s3_client_from_connection_store(self, connection_id: str, **kwargs) -> boto3.client:
        """
        Using a connection stored in the connection store, create and return a boto3 client configured with the
        credentials stored in the connection store

        :param connection_id: the UID of a connection stored in the connection store
        :param kwargs: additional keyword arguments to pass to the boto3.Session or boto3.client objects

        :return: a boto3.client('s3')
        """
    def is_pyvip_connected(self) -> bool:
        """
        Check if a User has an active pyvip connection to explore

        :return: bool
        """
    def save_datastore_asset(self, data: pandas.DataFrame, name: str, asset_id: str | None = None, description: str | None = '', overwrite_if_exists: bool = True, encode_columns: list | None = None, indexes: DatasetIndex | None = None):
        '''
        Write a pandas dataframe to a postgres table, and create an asset record. This allows for more efficient
        querying of the underlying data for certain use cases. Instead of being required to read the entire dataset
        into a dataframe in memory and perform transform, filter, select, etc. operations on the data. Instead this
        enables use of the `query_datastore_asset` function which allows for those operations to be executed in the db
        returning a smaller result set

        :param data: a pandas dataframe containing all the data to be written
        :param name: a name for this dataset, this should be a unique identifier that refers to the dataset
        :param asset_id: if overwriting an existing datastore asset, providing the asset_id specifies which asset will
                         be replaced
        :param description: a description of the asset, displayed in the `Assets` page
        :param overwrite_if_exists: overwrite the existing data with this name?
        :param indexes: an optional list of indexes to specify eg. `[{\'columns\': [\'column1\'], \'unique\': True}]`

        :return: the asset_id of the saved datastore asset


        **EXAMPLE:**

           .. code-block:: python
                import seaborn as sns

                from virtualitics_sdk import StoreInterface


                store_interface = StoreInterface(**flow_metadata)
                data = sns.load_dataset("iris")
                asset_id = store_interface.save_datastore_asset(
                    data=data, name="iris", indexes=[{"columns": ["sepal_length"], "unique": False}]
                )

        '''
    def query_datastore_asset(self, model: type[MappedAsDataclass | DeclarativeBase], select_: list['ColumnElement'] | None = None, where_: list['ColumnElement'] | None = None, name: str | None = None, asset_id: str | None = None) -> pandas.DataFrame:
        '''
        `       Query a previously saved datastore asset (saved with `StoreInterface.save_datastore_asset()`). Provide a
                SQLAlchemy BaseModel that describes the table where the asset is stored and optional select and where clauses.
                Returning a pandas dataframe that represents the ResultSet.

                :param model: A sqlalchemy Base model
                :param select_: a list of Column Expressions, any valid sqlalchemy column expression is acceptable, including sqlalchemy.func expressions
                :param where_: a list of Column Expressions to filter the dataset, any valid sqlalchemy column expression that resolves to a boolean value is acceptable, including sqlalchemy.func expressions
                :param name: the dataset asset name (either the asset name or the asset_id are required)
                :param asset_id: the dataset asset identifier (either the asset name or the asset_id are required)

                :return: a pandas dataframe with the serialized results of the query

                **EXAMPLE:**

                   .. code-block:: python

                        from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


                        class Base(MappedAsDataclass, DeclarativeBase):
                            pass


                        class Iris(Base):
                            __tablename__ = "iris"

                            id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
                            sepal_length: Mapped[Optional[float]] = mapped_column(sa.Double(53))
                            sepal_width: Mapped[Optional[float]] = mapped_column(sa.Double(53))
                            petal_length: Mapped[Optional[float]] = mapped_column(sa.Double(53))
                            petal_width: Mapped[Optional[float]] = mapped_column(sa.Double(53))
                            species: Mapped[Optional[str]] = mapped_column(sa.Text)


                        store_interface = StoreInterface(**flow_metadata)
                        df = store_interface.query_datastore_asset(
                            model=Iris,
                            name="iris",
                            select_=[Iris.sepal_length, Iris.sepal_width],
                            where_=[Iris.sepal_length > 0],
                        )
        '''
    def get_current_user_details(self) -> tuple[str, list[str]]:
        """
            Retrieve the details of the currently authenticated user.

            This function returns a tuple containing:
            - A string indicating the user's role.
            - A list of strings representing the names of the groups the user belongs to.


        :return: tuple[str, list[str]]: A tuple with the user's role and a list of associated group names.
        """
