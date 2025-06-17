from groq import Groq
from core.config import settings

llm = Groq(api_key=settings.GROQ_API_KEY)


def ask_llm(
    user_prompt,
    system_prompt="You are a helpful chatbot",
    model="llama-3.1-8b-instant",
    temperature=1,
):
    response = llm.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1,
        max_completion_tokens=1024,
    )
    return response.choices[0].message.content
