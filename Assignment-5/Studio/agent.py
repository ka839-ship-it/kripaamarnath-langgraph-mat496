import os
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq 
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode


os.environ["GROQ_API_KEY"] = "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"

def add(a: int, b: int) -> int:
    """Adds two numbers.

    Args:
        a: The first integer.
        b: The second integer.
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies two numbers.

    Args:
        a: The first integer.
        b: The second integer.
    """
    return a * b

def divide(a: int, b: int) -> float:
    """Divides two numbers.

    Args:
        a: The first integer (dividend).
        b: The second integer (divisor).
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

tools = [add, multiply, divide]

llm = ChatGroq(model="openai/gpt-oss-20b") 
llm_with_tools = llm.bind_tools(tools)


sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic operations. When performing arithmetic, think step by step.")


def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

graph = builder.compile()


if __name__ == "__main__":
    print("--- Running example 1: Add two numbers ---")
    inputs1 = {"messages": [("user", "What is 123 plus 456?")]}
    for s in graph.stream(inputs1):
        print(s)

    print("\n--- Running example 2: Multiply and then add ---")
    inputs2 = {"messages": [("user", "What is 7 times 8, and then add 5 to that result?")]}
    for s in graph.stream(inputs2):
        print(s)

    print("\n--- Running example 3: Complex calculation ---")
    inputs3 = {"messages": [("user", "Calculate (100 divided by 4) minus 15, then multiply by 2.")]}
    for s in graph.stream(inputs3):
        print(s)