# standard
# third party
import pydantic

# custom
from sunwaee_gen.model import Model
from sunwaee_gen.provider import Provider


class Error(pydantic.BaseModel):
    status: int = 0
    message: str = ""


class Usage(pydantic.BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Cost(pydantic.BaseModel):
    prompt_cost: float = 0.0
    completion_cost: float = 0.0
    total_cost: float = 0.0


class Performance(pydantic.BaseModel):
    latency: float = 0.0
    reasoning_duration: float = 0.0
    content_duration: float = 0.0
    total_duration: float = 0.0
    throughput: int = 0


class Response(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    model: Model
    provider: Provider
    error: Error = Error()
    usage: Usage = Usage()
    cost: Cost = Cost()
    performance: Performance = Performance()

    reasoning: str | None = None
    content: str | None = None
    tool_calls: list[dict] = []
    raw: str | None = None
    streaming: bool = False
