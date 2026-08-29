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

from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
import sqlite3
import operator

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['GROQ_API_KEY1']
    # other params...
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    CONFIG = {'configurable': {'thread_id': 'thread-2'}}
    response = chatbot.invoke(
    {'messages': [HumanMessage(content='My name is rohit how could yoy assist me?')]},
    config= CONFIG)

    print(response)

# InMemorySaver
#     ↓
# state lives in Python memory
#     ↓
# restart program
#     ↓
# ❌ state gone


# SqliteSaver
#     ↓
# state lives in SQLite database
#     ↓
# restart program
#     ↓
# ✅ state can be restored

def retrieve_all_threads():
    all_threads = set()
    ### checkpointer.list(None) include all the StateValueSnapshot
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

def num_threads():
    all_threads = set()
    ### checkpointer.list(None) include all the StateValueSnapshot
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return len(list(all_threads))
