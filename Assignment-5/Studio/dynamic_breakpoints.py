from typing_extensions import TypedDict
from langgraph.errors import NodeInterrupt
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    input: str

def step_1(state: State) -> State:
    print("---Step 1---")
    return state

def step_2(state: State) -> State:
    if len(state['input']) > 5:
        raise NodeInterrupt(f"Received input that is longer than 5 characters: {state['input']}")
    
    print("---Step 2---")
    return state

def step_3(state: State) -> State:
    print("---Step 3---")
    return state

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

graph = builder.compile()
#example
if __name__ == "__main__":
    print("--- Running dynamic_breakpoints example 1 (short input) ---")
    inputs1 = {"input": "hello"}
    for s in graph.stream(inputs1):
        print(s)

    print("\n--- Running dynamic_breakpoints example 2 (long input, will interrupt) ---")
    try:
        inputs2 = {"input": "superlonginput"}
        for s in graph.stream(inputs2):
            print(s)
    except NodeInterrupt as e:
        print(f"Graph interrupted: {e}")