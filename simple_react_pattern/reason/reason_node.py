from simple_react_pattern.graph_state import GraphState
from simple_react_pattern.reason.reason_prompt import reasoning_parser, reason_prompt_template
from simple_react_pattern.reason.reason_states import ReasoningState


def reason_node(state:GraphState,llm) -> GraphState:

    chain = reason_prompt_template | llm | reasoning_parser

    result : ReasoningState = chain.invoke(
        {
            'user_input':state.user_input,
            'context':state.context,
        }
    )

    #TODO : add the tests here
    state.current_step = state.current_step + 1

    state.next_tool_to_use = result.tool_to_call
    state.results=result.results
    state.user_request_fulfilled = result.user_request_fulfilled
    return state

