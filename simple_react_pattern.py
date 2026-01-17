'''

in react we will do the following :
user input :

reason will say get me the customer using the customer tool , the observer will
will check if we had all info we need,  if yes , return the resukts. else
we go to the reason again , with the user input , and our new info about the customer
then it will say , use the calculate totla ivestments tools

'''

'''
Limitations of this simple react :
What if the user input requires a tool we have not implemented yet ???
'''

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from llm import get_groq_llm
from simple_react_pattern.act.act_node import act_node
from simple_react_pattern.condition_function import should_continue
from simple_react_pattern.graph_state import GraphState
from simple_react_pattern.observe.observe_node import observe_node
from simple_react_pattern.reason.reason_node import reason_node
from simple_react_pattern.tools import tools

llm = get_groq_llm()




def build_graph(llm,tools):
    graph = StateGraph(GraphState)
    graph.add_node("reason_node", lambda s: reason_node(s, llm))
    graph.add_node("act_node", lambda s: act_node(s, tools))
    graph.add_node('observe_node',lambda s:observe_node(s))

    graph.add_edge(START, "reason_node")
    graph.add_conditional_edges(
        "reason_node",
        should_continue,
        {
            "act_node": "act_node",
            "end": END,
        },
    )
    graph.add_edge("act_node", "observe_node")
    graph.add_edge("observe_node", 'reason_node')

    return graph.compile()


app = build_graph(llm,tools)


mermaid = app.get_graph().draw_mermaid()
with open("graph.mmd", "w") as f:
    f.write(mermaid)

#
# init_state = GraphState(
#     user_input='get me the customer total investments and the customer user_type for customer with an id of 1',
# )
#
# res = app.invoke(init_state)
#
# print(res['results'])



