import random
from openai import OpenAI
from app.config import settings

SYSTEM_PROMPT = """
You are Kroz, an intelligent assistant created by devkroz.
You help users with questions, tasks, and problems.
Be concise, helpful, and friendly. Respond in the same language the user writes to you.
"""

_fallback_responses = [
    "Interessante! Me pergunte algo específico que posso ajudar melhor.",
    "Entendi! Pode me dar mais detalhes?",
    "Ótima pergunta! Vou pesquisar sobre isso pra você.",
    "Hmm, deixe-me pensar... Qual é o contexto disso?",
]

client = None
if settings.openai_api_key and settings.openai_api_key != "sk-your-key-here":
    client = OpenAI(api_key=settings.openai_api_key)


def ask(message: str, history: list[dict] | None = None) -> str:
    if client is None:
        return random.choice(_fallback_responses)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content
