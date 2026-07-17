import os
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from typing import Literal, Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START, END  

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
import operator

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=os.environ['GROQ_API_KEY2']
    # other params...
)


from langgraph.graph.message import add_messages

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    # response store state
    return {'messages': [response]}


graph = StateGraph(ChatState)
checkpointer = InMemorySaver()
# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

for message_chunk , meta_data in chatbot.stream(
    {'messages' : [HumanMessage(content = "Receipe to make pasta??")]},
    config = {'configurable' : {'thread_id' : 1}},
    stream_mode="messages"
):
    if message_chunk.content:
        print(message_chunk.content, end = " ", flush=True)


