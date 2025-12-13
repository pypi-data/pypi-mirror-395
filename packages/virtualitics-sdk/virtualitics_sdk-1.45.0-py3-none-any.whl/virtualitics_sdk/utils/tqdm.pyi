from _typeshed import Incomplete
from tqdm import tqdm as base_tqdm
from typing import Callable
from virtualitics_sdk import FlowMetadata as FlowMetadata

class StepProgressTqdm(base_tqdm):
    '''
    It is a tqdm wrapper that accept some parameters to update the
    front-end progress bar accordingly to the progress made in tqdm.

    In addition to the classic tqdm init parameters it accepts a
    reference to the store interface and apply the update_progress call.

    :param flow_metadata: The app metadata necessary to create a store interface.
    :param total: Number of elements.
    :param starting_progress: Progress starting point, defaults to 0.
    :param target_progress: It is the target progress the tqdm engine will reach, defaults to 100.
    :param callback: Function that changes the default StepProgressTqdm manual update.
    :param call_super_update: Whether by default the update method should call the default tqdm update method,
                            defaults to True.
    :param init_update: An optional first update string to display before the first iteration of the loop has
                            completed, defaults to None.
    :param **kwargs: All the parameters the tqdm init exposes.

    **EXAMPLE**

        .. code-block:: python

            # Imports
            from virtualitics_sdk.utils.tqdm import StepProgressTqdm
            . . .

            # Example usage
            . . .

            class ExStep(Step):
                def run(self, flow_metadata):
                    . . .
                    progress_bar = StepProgressTqdm(flow_metadata,
                                                    starting_progress=0,
                                                    target_progress=100,
                                                    total=100,
                                                    step_size=10,
                                                    desc="My progress bar",
                                                    init_update="Starting my progress bar...")
                    . . .
                    for i in range(100):
                        progress_bar.update(1)
    '''
    store: Incomplete
    step_size: Incomplete
    starting_progress: Incomplete
    target_progress: Incomplete
    callback: Incomplete
    call_super_update: Incomplete
    def __init__(self, flow_metadata: FlowMetadata, total: int, starting_progress: int | float = 0, target_progress: int | float = 100, step_size: int = 10, callback: Callable | None = None, call_super_update: bool = True, init_update: str | None = None, **kwargs) -> None: ...
    def update(self, n: int | float = 1):
        """
        Override the base update method. Useful for manual updates.
        If no store is provided, it will only call the super.update implementation
        otherwise it will perform an update to the front-end, calling the update_progress
        function.

        :param n: Default increment, defaults to 1.

        """
