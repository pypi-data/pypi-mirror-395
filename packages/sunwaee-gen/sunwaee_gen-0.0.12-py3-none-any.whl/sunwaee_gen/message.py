# standard
import json
import typing

# third party
import pydantic

# custom
from sunwaee_gen.tool_call import ToolCall


class Message(pydantic.BaseModel):
    role: typing.Literal["system", "user", "assistant", "tool"]
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    def to_dict(self) -> dict:
        res = {
            "role": self.role,
            "content": self.content,
        }

        # optional
        if self.tool_calls:
            res["tool_calls"] = [tc.model_dump() for tc in self.tool_calls]

        # optional
        if self.tool_call_id:
            res["tool_call_id"] = self.tool_call_id

        return res

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        if "role" not in data or "content" not in data:
            raise ValueError("Message requires 'role' and 'content'")

        # optional
        tool_calls = None
        if "tool_calls" in data:
            if not isinstance(data["tool_calls"], list):
                raise ValueError("'tool_calls' must be a list of dicts")
            tool_calls = [ToolCall.from_dict(tc) for tc in data["tool_calls"]]

        return cls(
            role=data["role"],
            content=data["content"],
            tool_call_id=data.get("tool_call_id"),
            tool_calls=tool_calls,
        )

    @classmethod
    def from_list(cls, items: list[dict]) -> "list[Message]":
        return [cls.from_dict(item) for item in items]
