from simple_react_pattern.graph_state import GraphState
from simple_react_pattern.observe.observe_node import observe_node
from simple_react_pattern.reason.reason_states import ToolToCall
from simple_react_pattern.tools import Customer

mock_state = GraphState(
user_input='test',
    next_tool_to_use=ToolToCall(tool_returned_value='customer_object', tool_name='get_customer_from_db', arguments={'customer_id': '1'}, tool_description='fetch a customer by customer id from our database and returns it') ,
    context={} ,
    last_tool_result=Customer(id='1', name='Test Customer from db', investments=[50], user_type='nbk_invest')

)

expected_state = GraphState(
user_input='test',
    next_tool_to_use=None,
    context={'customer_object': Customer(id='1', name='Test Customer from db', investments=[50], user_type='nbk_invest')},
    last_tool_result=None,

)



class TestObserveNode:

    def test_observe_node(self):

        res = observe_node(mock_state)
        assert res == expected_state
