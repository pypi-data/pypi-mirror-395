from _typeshed import Incomplete
from typing import TypeAlias
from virtualitics_sdk.app.step import Step as Step
from virtualitics_sdk.llm.agent import DispatcherAgentInterface as DispatcherAgentInterface

logger: Incomplete

class App:
    '''An App represent a workflow in the Virtualitics AI Platform. An App can contain many :class:`~virtualitics_sdk.flow.step.Step`\'s that can
    get inputs, run computation, and show results.

    :param name: The name of the App.
    :param description: The App description
    :param image_path: The base64 encoding of an image or a public link to an image, defaults to None
    :param is_shareable: Whether a given App is shareable, defaults to False
    :param sort_key: An optional value to sort the App by, this controls the sort order of Apps on the home page
    :param on_llm_request: An optional async function to pre-process data before sending to an LLM.
    :param on_llm_response: An optional async function to post-process data after receiving it from an LLM.
    :param default_prompts: A list of default prompt suggestions to show in IRIS to users of the app


    **EXAMPLE:**

       .. code-block:: python

           # Imports
           from virtualitics_sdk import App
           . . .
           # Example usage
           tile_image_link = "https://example-image.jpeg"
           example_flow = App(name="Example App",
                                     description="Simple example for using App class",
                                     image_path=tile_image_link)
    '''
    id: Incomplete
    title: Incomplete
    name: Incomplete
    description: Incomplete
    last_run_step: Incomplete
    step_map: dict[str, Step]
    steps: list[Step]
    is_locked: bool
    is_complete: bool
    image: Incomplete
    is_shareable: Incomplete
    sort_key: Incomplete
    agent: Incomplete
    def __init__(self, name: str, description: str, image_path: str | None = None, is_shareable: bool = False, sort_key: str | None = None, agent: DispatcherAgentInterface | None = None) -> None: ...
    def chain(self, ordered_steps: list[Step], lock: bool = True):
        """Add all steps to the App's workflow with one function. Locks Apps by default.

        :param ordered_steps: Ordered list of Steps to be added.
        """
    def get_data(self, app_id: str | None = None): ...
Flow: TypeAlias = App
