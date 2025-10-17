import random
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
import os

# Set Groq API Key (replace with your actual key or environment variable)
os.environ["GROQ_API_KEY"] = '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'

# Initialize LLM (Groq) and Embeddings (Hugging Face) globally or pass them
# *** IMPORTANT: UPDATED MODEL NAME HERE AGAIN ***
# Please verify current models at https://console.groq.com/docs/models
llm = ChatGroq(model="moonshotai/kimi-k2-instruct") # Changed to a currently supported model
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# State
class State(TypedDict):
    graph_state: str
    mood_score: float # Added to show how LLM might influence state

# Conditional edge (remains largely the same, but could now use mood_score)
def decide_mood(state) -> Literal["node_2", "node_3"]:
    print(f"---Deciding Mood based on score: {state.get('mood_score', 0.5)}---")
    # Now, let's use the mood_score from the LLM if available, otherwise fallback to random
    if state.get('mood_score') is not None:
        if state['mood_score'] > 0.5: # Higher score = happy
            return "node_2"
        else: # Lower score = sad
            return "node_3"
    else:
        # Fallback to random if mood_score isn't set
        if random.random() < 0.5:
            return "node_2"
        return "node_3"

# Nodes
def node_1(state):
    print("---Node 1: Initializing and asking LLM for sentiment---")
    current_input = state.get('graph_state', 'The user feels...')

    # Use the LLM to get a sentiment for the initial state
    try:
        # Craft a prompt to get a sentiment score
        prompt = f"Analyze the sentiment of the following text and provide a score between 0.0 and 1.0, where 0.0 is very negative and 1.0 is very positive. Only output the score:\nText: '{current_input}'"
        response = llm.invoke([HumanMessage(content=prompt)])
        mood_score_str = response.content.strip()

        try:
            mood_score = float(mood_score_str)
            # Ensure score is within 0-1 range
            mood_score = max(0.0, min(1.0, mood_score))
        except ValueError:
            print(f"Warning: LLM returned non-numeric mood score: '{mood_score_str}'. Defaulting to 0.5.")
            mood_score = 0.5

    except Exception as e:
        print(f"Error calling LLM in node_1: {e}. Defaulting mood_score to 0.5.")
        mood_score = 0.5

    new_graph_state = current_input + " I am"
    return {"graph_state": new_graph_state, "mood_score": mood_score}

def node_2(state):
    print("---Node 2: Processing 'Happy' path with LLM---")
    current_state = state['graph_state']
    # Use LLM to elaborate on the happy feeling
    try:
        prompt = f"Given the current state '{current_state}', expand on a happy feeling. Keep it concise, one sentence."
        response = llm.invoke([HumanMessage(content=prompt)])
        happy_response = response.content.strip()
    except Exception as e:
        print(f"Error calling LLM in node_2: {e}. Using default happy message.")
        happy_response = "happy!"

    return {"graph_state": current_state + " " + happy_response, "mood_score": 0.8}

def node_3(state):
    print("---Node 3: Processing 'Sad' path with LLM---")
    current_state = state['graph_state']
    # Use LLM to elaborate on the sad feeling
    try:
        prompt = f"Given the current state '{current_state}', expand on a sad feeling. Keep it concise, one sentence."
        response = llm.invoke([HumanMessage(content=prompt)])
        sad_response = response.content.strip()
    except Exception as e:
        print(f"Error calling LLM in node_3: {e}. Using default sad message.")
        sad_response = "sad!"

    return {"graph_state": current_state + " " + sad_response, "mood_score": 0.2}

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Compile graph
graph = builder.compile()

# Example Usage
if __name__ == "__main__":
    # Function to run the graph and print results cleanly
    def run_scenario(initial_state: str):
        print(f"\n--- Running Graph (Initial state: '{initial_state}') ---")
        last_state = None
        for s in graph.stream({"graph_state": initial_state}):
            print(s)
            last_state = s # Keep track of the last state
        if last_state:
            # When END is reached, the state will be under the '__end__' key
            # but for stream, the last output is just the node that leads to END.
            # To get the final accumulated state, we can use invoke or simply print the last node's output.
            # If the graph has a single path to END, the 'last_state' will be the output of the node that connects to END.
            # If you want the *full* final accumulated state, graph.invoke() is better.
            print("Final state (from last streamed node):", last_state)

        # Alternatively, to get the full final state without streaming
        # final_full_state = graph.invoke({"graph_state": initial_state})
        # print("Final state (from invoke):", final_full_state)


    run_scenario("I feel great today.")
    run_scenario("Today is a bad day.")
    run_scenario("The weather is okay.") # This might still use the random fallback if LLM sentiment is exactly 0.5