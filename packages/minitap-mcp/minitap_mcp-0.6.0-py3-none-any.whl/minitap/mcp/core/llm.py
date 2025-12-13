from langchain_openai import ChatOpenAI

from minitap.mcp.core.config import settings


def get_minitap_llm(
    trace_id: str,
    remote_tracing: bool = False,
    model: str = "google/gemini-2.5-pro",
    temperature: float | None = None,
    max_retries: int | None = None,
) -> ChatOpenAI:
    assert settings.MINITAP_API_KEY is not None
    assert settings.MINITAP_API_BASE_URL is not None
    if max_retries is None and model.startswith("google/"):
        max_retries = 2
    client = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_retries=max_retries,
        api_key=settings.MINITAP_API_KEY,
        base_url=settings.MINITAP_API_BASE_URL,
        default_query={
            "sessionId": trace_id,
            "traceOnlyUsage": remote_tracing,
        },
    )
    return client


def get_openrouter_llm(model_name: str, temperature: float = 1):
    assert settings.OPEN_ROUTER_API_KEY is not None
    client = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=settings.OPEN_ROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    return client
