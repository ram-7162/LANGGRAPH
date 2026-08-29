from langgraph.graph import StateGraph, START
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from chatmodel_groq import chatbot
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()  # Load environment variables from .env file
llm = chatbot


loader = PyPDFLoader("intro-to-ml.pdf")
doc = loader.load()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # small, fast, good default
)

vectorstore = Chroma.from_documents(
    documents=doc,
    embedding=embedding_model,
    collection_name="my_collection"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


@tool
def rag_tool(query):
    """
    Retrieve relevant information from the pdf document.
    Use this tool when the user asks factual / conceptual questions
    that might be answered from the stored documents.
    """
    result = retriever.invoke(query)
    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]
    return {
        'query': query,
        'context': context,
        'metadata': metadata
    }



tools = [rag_tool]

llm_with_tools = llm.bind_tools(tools)

# state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# nodes
def chat_node(state: ChatState):

    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

tool_node = ToolNode(tools)

# defining graph and nodes
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

# defining graph connections
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile()

# running the graph
result = chatbot.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Using the pdf notes, explain how to find the ideal value of K in KNN"
                )
            )
        ]
    }
)

print(result['messages'][-1].content)











