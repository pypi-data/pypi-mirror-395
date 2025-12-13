from typing import TypedDict

class FlowMetadata(TypedDict):
    flow_id: str
    step_name: str
    user: str
    is_action: bool
