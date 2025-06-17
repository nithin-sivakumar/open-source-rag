from langgraph.graph import StateGraph, START, END
from nodes.chatbot import chatbot
from langgraph.checkpoint.memory import InMemorySaver
from tools.rag_agent import rag_agent
from utils.state import CustomState

checkpointer = InMemorySaver()


graph_builder = StateGraph(CustomState)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("rag", rag_agent)

graph_builder.add_edge(START, "rag")
graph_builder.add_edge("rag", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=checkpointer)
