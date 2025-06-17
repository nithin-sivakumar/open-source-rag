from utils.state import CustomState
from utils.llm_service import ask_llm
from langchain_core.messages import AIMessage


def chatbot(state: CustomState):
    prompt = f"""
    You are an intelligent chatbot agent. Respond to the user's message accordingly

    User message: {state['messages'][-2]}
    Context: {state['messages'][-1]}
    Metdata: {state['metadata']}

    Message history (use if needed): {state['messages']}

    Respond like a chatbot would, return simple straightforward answers
    
    If context is not relevant to the user's query, respond clearly and politely stating that you don't know,
    do not assume anything or hallucinate. Don't give general responses.
    If data is available, respond to it, if not, reject the request stating the reason
    """
    response = ask_llm(prompt, model="")

    return {"messages": AIMessage(response)}  # type: ignore
