from dataclasses import dataclass, field
from langchain_core.tools import tool

from simple_react_pattern.helpers.available_tools_description import get_available_tools_description


@dataclass
class Customer:
    id:str
    name:str
    investments: list[float] = field(default_factory=list)
    user_type:str=None



@tool(
    description="fetch a customer by customer id from our database and returns it"
)
def get_customer_from_db(customer_id: str) -> Customer:

    '''Mock Data That should come from the database'''
    return Customer(
        id='1',
        name="Test Customer from db",
        investments=[50],
        user_type='merchant'
    )


@tool(description="accepts a customer object and returns the summation of the customer investments")
def calculate_customer_total_investments(customer:Customer) -> int:
    total_investments = sum(customer.investments)
    return total_investments

@tool(description="accepts a customer object and returns the user_type of the customer")
def get_customer_user_type(customer:Customer) -> str:
    return customer.user_type



tools = [get_customer_from_db,calculate_customer_total_investments,get_customer_user_type]

available_tools_description = get_available_tools_description(tools)
