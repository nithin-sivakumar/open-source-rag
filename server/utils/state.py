from langgraph.graph import MessagesState


class CustomState(MessagesState):
    metadata: list
    session_id: str
