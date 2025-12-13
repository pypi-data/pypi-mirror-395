from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from virtualitics.api import VIP as VIP
from virtualitics_sdk import App as App, Page as Page
from virtualitics_sdk.app.flow_metadata import FlowMetadata as FlowMetadata
from virtualitics_sdk.llm.agent import DispatcherAgentInterface as DispatcherAgentInterface

class StepType(Enum):
    """The type of Step being created.
    INPUT: A Step should be of type input if it contains input elements.
    DASHBOARD: Marking steps as Dashboard Steps helps them be easily found in the Dashboards section.
    RESULTS: If a step contains neither inputs or dashboards it should be a Results step.
    """
    INPUT: int
    DATA_LAB: int
    RESULTS: int
    DASHBOARD: int

class Step(ABC):
    """A Step is the basic unit of an app. Steps can be chained together to form an app.

    :param title: The title of the step.
    :param description: A description of what the step does.
    :param parent: The parent step.
    :param type: The Step type.
    :param page: The initial Page for this step.
    :param uses_pyspark: Whether or not the step uses PySpark, defaults to False.
    :param uses_pyvip: Whether or not the step requires a pyVIP connection, defaults to False.
    :param uses_snowflake: Whether or not the step requires a Snowflake connection, defaults to False.
    :param overrides_action: Whether this step overrides the default action for this step type, defaults to False.
    :param await_actions: whether this step overrides must wait for an action to continue to the next page, defaults to True.
    :param override_skips_default: When true and overrides_action is true, this flag defines whether to skip over the default step action, defaults to False.
    :param alerts: The Alerts for this Step. This feature is currently unimplemented, defaults to None.
    :param default_max_memory_usage: The default maximum memory usage of this step in bytes
    :param on_llm_request: An optional async function to pre-process data before sending to an LLM.
    :param on_llm_response: An optional async function to post-process data after receiving it from an LLM.
    :param default_prompts: A list of default prompt suggestions to show in IRIS to users of the app
    :param show_title: Whether to show the title on the page when rendered, defaults to True.
    :raises PredictException: Raises an error if the character '/' is found in the flow title.
    """
    title: Incomplete
    name: Incomplete
    description: Incomplete
    parent: Incomplete
    type: Incomplete
    page: Incomplete
    allow_filters: Incomplete
    state: Incomplete
    overrides_action: Incomplete
    await_actions: Incomplete
    override_skips_default: Incomplete
    uses_pyvip: Incomplete
    uses_pyspark: Incomplete
    pyspark_config: Incomplete
    spark_session: Incomplete
    uses_snowflake: Incomplete
    alerts: Incomplete
    extra_keyword_args: Incomplete
    last_step: bool
    default_max_memory_usage: Incomplete
    agent: Incomplete
    show_title: Incomplete
    def __init__(self, title: str, description: str, parent: str, type: StepType, page: Page, allow_filters: bool = False, uses_pyspark: bool = False, uses_pyvip: bool = False, uses_snowflake: bool = False, overrides_action: bool = False, await_actions: bool = True, override_skips_default: bool = False, alerts: list | None = None, default_max_memory_usage: int = None, agent: DispatcherAgentInterface | None = None, show_title: bool = True, **kwargs) -> None: ...
    def copy(self): ...
    @property
    def progress(self): ...
    @progress.setter
    def progress(self, val: int): ...
    @property
    def message(self): ...
    @message.setter
    def message(self, val: str): ...
    def progress_update(self, progress: int, message: str): ...
    @abstractmethod
    def run(self, flow_metadata: FlowMetadata, spark_session=None, pyvip_client: VIP | None = None): ...
    def action_override(self, flow_metadata: FlowMetadata):
        '''
        This method is similar to :class:`~virtualitics_sdk.flow.step.Step.run`, but is not mandatory to implement
        in a given Step. It allows for the customization or bypassing of default step actions.

        Typically, when a step runs, all code in the run method executes before the page is generated,
        and upon clicking the "Next" button, the step action executes to clean up and prepare for the next step.
        This method is useful for scenarios where the default action, such as processing a .csv file into a Pandas DataFrame,
        needs to be customized or skipped entirely.

        Overriding this method in a step will run this function after the step has
        been completed. To make sure this runs, set `overrides_action` to True. If you
        want to skip the default behavior for an action (i.e. for custom data processing of
        an input file), set override_skips_default to True as well.

        :param flow_metadata: Relevant information about the current step which is useful to access the :class:`~virtualitics_sdk.store.store_interface.StoreInterface`

        **EXAMPLE:**

           .. code-block:: python

               # Imports
               from virtualitics_sdk import Step

               ...


               # Example usage
               class DataUpload(Step):
                   def run(self, flow_metadata):
                       pass

                   def action_override(self, flow_metadata):
                       query_id = store_interface.get_element_value(data_upload_step.name, "Query Selection")
                       query = QUERY_SELECTION.get(query_id)
                       df = store_interface.db_to_pandas(query, conn_name="shotlogs")
                       store_interface.save_output(df, DATA_LINK)
        '''
    def on_run_success(self, store_interface, *args, **kwargs) -> None: ...
    def on_action_success(self, store_interface, *args, **kwargs) -> None: ...
    def on_cancel(self, store_interface) -> None: ...
    async def on_failure(self, store_interface) -> None: ...
