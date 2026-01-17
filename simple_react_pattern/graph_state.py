from typing import Optional, Any

from pydantic import BaseModel, Field

from simple_react_pattern.reason.reason_states import ToolToCall


class GraphState(BaseModel):
    user_input:str
    next_tool_to_use:Optional[ToolToCall] = None
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Shared context for intermediate tool results (e.g. {'customer': Customer})"
    )
    last_tool_result: Any = None  # temporary storage between Act and Observe
    user_request_fulfilled : bool = Field(default=False , description='This will indicates if the user request is fulfilled or not')
    results : Any = Field(description='The final results if the user request is fulfilled' , default=None)
    current_step:int=0
