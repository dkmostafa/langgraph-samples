from typing import Optional, Any

from pydantic import BaseModel, Field


class ToolToCall(BaseModel):
    tool_returned_value: str = Field(description="The business semantic name for the value of what my tool will return")
    tool_name: str = Field(description="The exact name of the tool to call")
    arguments: dict = Field(description="The tool accepted arguments and their values ") #todo : may change the parameters field name to args
    tool_description: str = Field(description="what does the tool do?")



class ReasoningState(BaseModel):
    reason_thought :str =Field(description="Step-by-step reasoning as short bullet points" , default="")
    tool_to_call: Optional[ToolToCall] = Field(
        description="The single tool to be called for this step, or null if no tool is required",
        default=None
    )
    results : dict[str, Any] = Field(
        default_factory=dict,
        description="The final results of the user_input store as a dict"
    )
    user_request_fulfilled : bool = Field(default=False , description='This will indicates if the user request is fulfilled or not')
