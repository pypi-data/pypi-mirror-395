# standard
import json

# third party
import fastapi
import pydantic
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# custom
from sunwaee_gen import (
    Agent,
    AGENTS,
    Provider,
    PROVIDERS,
    Model,
    Message,
    Response,
    Tool,
    MODELS,
    async_completion,
)

api = fastapi.FastAPI(
    title="Sunwaee GEN API",
    summary="All LLMS, one response format.",
    version="0.0.1",
)


# --- GET


@api.get("/agents", response_model=list[Agent])
async def list_available_agents():
    """List available agents with naming format `provider/model` (e.g. 'anthropic/claude-4-sonnet', 'openai/gpt-5'...)"""
    return [a for a in AGENTS.values()]


@api.get("/providers", response_model=list[Provider])
async def list_available_providers():
    """List available providers (e.g. 'anthropic', 'openai'...)"""
    return [p for p in PROVIDERS.values()]


@api.get("/models", response_model=list[Model])
async def list_available_models():
    """List available models (e.g. 'claude-4-sonnet', 'gpt-5'...)"""
    return [m for m in MODELS.values()]


# --- POST


class CompletionRequest(pydantic.BaseModel):
    agent: str
    messages: list[Message]
    tools: list[Tool] | None
    streaming: bool = False


@api.post("/completion", response_model=Response)
async def llm_completion(
    req: CompletionRequest,
    credentials: HTTPAuthorizationCredentials = fastapi.Depends(
        HTTPBearer(auto_error=True)
    ),
):
    """All LLMs, one response format."""

    # NOTE no api_key -> 403
    api_key = credentials.credentials

    agent = req.agent
    messages = [m.to_dict() for m in req.messages]
    tools = [t.model_dump() for t in req.tools] if req.tools else None
    streaming = req.streaming

    if streaming:

        async def event_generator():
            async for chunk in async_completion(
                agent=agent,
                api_key=api_key,
                messages=messages,
                tools=tools,
                streaming=True,
            ):
                yield json.dumps(chunk) + "\n"

        return StreamingResponse(event_generator(), media_type="application/json")

    else:

        async for chunk in async_completion(
            agent=agent,
            api_key=api_key,
            messages=messages,
            tools=tools,
            streaming=False,
        ):
            return chunk
