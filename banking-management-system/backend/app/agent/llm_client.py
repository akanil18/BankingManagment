from openai import AsyncOpenAI
from app.config import settings

# llama-server exposes an OpenAI-compatible API
llm_client = AsyncOpenAI(
    base_url=settings.LLAMA_SERVER_URL,
    api_key="not-required",  # llama-server does not need a real key
)


async def chat(messages: list, temperature: float = None, max_tokens: int = None) -> str:
    response = await llm_client.chat.completions.create(
        model=settings.LLAMA_MODEL_NAME,
        messages=messages,
        temperature=temperature or settings.LLAMA_TEMPERATURE,
        max_tokens=max_tokens or settings.LLAMA_MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()
