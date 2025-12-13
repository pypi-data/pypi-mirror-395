from virtualitics_sdk.store.store_interface import StoreInterface as StoreInterface

async def trigger_flow_execution(flow_name: str, store_interface: StoreInterface, input_parameters: dict | None = {}):
    """
    A utility function to trigger the execution of another app (to be run headless). For example trigger the
    execution of another app upon the completion of a different app.

    :param flow_name: The name of the app to trigger. App names are usually CamelCaseNames.
    :param store_interface: The StoreInterface to pass metadata about the app execution environment.
    :param input_parameters: Additional input parameters to pass to the triggered app
    """
