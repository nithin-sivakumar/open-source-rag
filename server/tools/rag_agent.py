from utils.state import CustomState
from langchain_core.messages import AIMessage
from utils.vector_service import vector_store


def rag_agent(state: CustomState):
    session = state["session_id"]

    results = vector_store.similarity_search(
        str(state["messages"][-1].content),
        k=5,
        pre_filter={"session_id": session},
    )

    response = ""

    for result in results:
        response += result.page_content + "\n\n"

    return {"messages": AIMessage(response), "metadata": [item.metadata for item in results]}  # type: ignore
