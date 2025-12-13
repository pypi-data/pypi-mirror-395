from _typeshed import Incomplete
from virtualitics_sdk import Element as Element, Row as Row
from virtualitics_sdk.page.card import Card as Card

class DrilldownStoreInterface:
    flow_id: Incomplete
    user_id: Incomplete
    step_name: Incomplete
    card: Incomplete
    def __init__(self, flow_id: str, user_id: str, step_name: str, card: Card) -> None: ...
    def add_element(self, *, elements: Row | list[Element] | Element, ratio: list[int | float] | None = None, index: int | None = None): ...
    @staticmethod
    def update_progress(completion: float | int, message: str):
        """
        Update the progress of the drilldown callback as it's running. It is recommended to use this 
        when steps have operations that can take a long time.

        :param completion: The progress to completion (0 to 100).
        :param message: The message to show at this level of completion.
        """
    @staticmethod
    async def aupdate_progress(completion: float | int, message: str):
        """
        Update the progress of the drilldown callback as it's running. It is recommended to use this 
        when steps have operations that can take a long time.

        :param completion: The progress to completion (0 to 100).
        :param message: The message to show at this level of completion.
        """
