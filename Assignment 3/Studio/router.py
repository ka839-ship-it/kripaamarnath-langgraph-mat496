from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Make sure to set your API keys as environment variables or pass them directly
# For Groq
import os
os.environ["GROQ_API_KEY"] = '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'
# Hugging Face doesn't strictly need an API key for local embeddings,
# but if you were using a hosted inference endpoint, you might need one.

# Tool (remains the same)
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# LLM with bound tool using Groq
# We're using ChatGroq here instead of ChatOpenAI
llm = ChatGroq(model="moonshotai/kimi-k2-instruct") # You can choose a different Groq model
llm_with_tools = llm.bind_tools([multiply])

# Hugging Face Embeddings
# You can choose a different model from the Hugging Face model hub
# For example, "sentence-transformers/all-MiniLM-L6-v2" is a good general-purpose model.
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Node (remains mostly the same, just the LLM instance changes)
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph (remains the same)
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", END)

# Compile graph (remains the same)
graph = builder.compile()

# Example usage (to demonstrate both LLM and embeddings)
if __name__ == "__main__":
    # Test the graph with the Groq LLM and tool
    print("--- Testing the Graph with Groq LLM ---")
    inputs = {"messages": [HumanMessage(content="What is 7 times 8?")]}
    for s in graph.stream(inputs):
        print(s)

    inputs_no_tool = {"messages": [HumanMessage(content="Hello, how are you?")]}
    for s in graph.stream(inputs_no_tool):
        print(s)

    # Test the Hugging Face embeddings
    print("\n--- Testing Hugging Face Embeddings ---")
    texts = [
        "This is a test sentence.",
        "This sentence is about testing.",
        "Another unrelated sentence."
    ]
    document_embeddings = hf_embeddings.embed_documents(texts)
    query_embedding = hf_embeddings.embed_query("What is this about?")

    print(f"Embeddings for documents (first 5 dimensions of first document): {document_embeddings[0][:5]}...")
    print(f"Embedding for query (first 5 dimensions): {query_embedding[:5]}...")

    # You can now use these embeddings for similarity searches, RAG, etc.