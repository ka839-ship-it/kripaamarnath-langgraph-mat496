# Make sure these lines are at the very top of your file,
# before any other code that tries to use GROQ_API_KEY
GROQ_API_KEY = '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'
OPENAI_API_KEY = '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'

import os # Good practice to import os if you intend to use os.environ later
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]

# Define LLM with bound tools
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY, # This is where it needs GROQ_API_KEY to be defined above
    model_name="moonshotai/kimi-k2-instruct"
)
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with writing performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()

if __name__ == "__main__":
    inputs = {"messages": [("user", "What is 10 + 5?")]}
    result = graph.invoke(inputs)
    print(result["messages"][-1].content)

    inputs_multiply = {"messages": [("user", "Multiply 7 by 3.")]}
    result_multiply = graph.invoke(inputs_multiply)
    print(result_multiply["messages"][-1].content)