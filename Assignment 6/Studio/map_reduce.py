#map_reduce.py
import operator
from typing import Annotated
from typing_extensions import TypedDict
import os

from pydantic import BaseModel

from langchain_groq import ChatGroq # Changed from langchain_openai
from langchain_community.embeddings import HuggingFaceEmbeddings # Changed from langchain_openai

from langgraph.constants import Send
from langgraph.graph import END, StateGraph, START

# Prompts we will use
subjects_prompt = """Generate a list of 3 sub-topics that are all related to this overall topic: {topic}. For example if the topic is 'Space Exploration', sub-topics could be 'Mars Rovers', 'Exoplanet Discovery', 'Space Telescopes'. Make sure the sub-topics are distinct and interesting."""
story_prompt = """Generate a short, engaging story (around 150 words) about {subject}. Focus on a unique character and an interesting conflict or discovery."""
best_story_prompt = """Below are a bunch of short stories about {topic}. Select the best one based on creativity, coherence, and engagement. Return the ID of the best one, starting 0 as the ID for the first story. Stories: \n\n  {stories}"""

# LLM
# Changed to Groq and using an environment variable for the API key
model = ChatGroq(temperature=0, model_name="llama3-8b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

# Embedding model (Hugging Face)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Define the state
class Subjects(BaseModel):
    subjects: list[str]

class BestStory(BaseModel):
    id: int
    
class OverallState(TypedDict):
    topic: str
    subjects: list
    stories: Annotated[list, operator.add]
    best_selected_story: str

def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}

class StoryState(TypedDict):
    subject: str

class Story(BaseModel):
    story: str

def generate_story(state: StoryState):
    prompt = story_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Story).invoke(prompt)
    return {"stories": [response.story]}

def best_story(state: OverallState):
    stories = "\n\n".join(state["stories"])
    prompt = best_story_prompt.format(topic=state["topic"], stories=stories)
    response = model.with_structured_output(BestStory).invoke(prompt)
    return {"best_selected_story": state["stories"][response.id]}

def continue_to_stories(state: OverallState):
    return [Send("generate_story", {"subject": s}) for s in state["subjects"]]

# Construct the graph: here we put everything together to construct our graph
graph_builder = StateGraph(OverallState)
graph_builder.add_node("generate_topics", generate_topics)
graph_builder.add_node("generate_story", generate_story)
graph_builder.add_node("best_story", best_story)
graph_builder.add_edge(START, "generate_topics")
graph_builder.add_conditional_edges("generate_topics", continue_to_stories, ["generate_story"])
graph_builder.add_edge("generate_story", "best_story")
graph_builder.add_edge("best_story", END)

# Compile the graph
graph = graph_builder.compile()