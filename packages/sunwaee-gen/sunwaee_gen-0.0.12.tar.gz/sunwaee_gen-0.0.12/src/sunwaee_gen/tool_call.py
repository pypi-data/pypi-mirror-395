# standard
import json

# third party
import pydantic

# custom


class Function(pydantic.BaseModel):
    name: str
    arguments: str


class ToolCall(pydantic.BaseModel):
    id: str
    type: str = pydantic.Field(default="function")
    function: Function

    @classmethod
    def from_dict(cls, data: dict) -> "ToolCall":
        if "id" not in data or not data["id"]:
            raise ValueError("Tool call requires a non-empty 'id'")
        if "function" not in data or not isinstance(data["function"], dict):
            raise ValueError(
                "Tool call requires a 'function' object with 'name' and 'arguments'"
            )

        func = data["function"]

        if "name" not in func or not func["name"]:
            raise ValueError("Tool call 'function' requires a non-empty 'name'")
        if "arguments" not in func:
            raise ValueError("Tool call 'function' requires 'arguments'")

        args = func["arguments"]
        if isinstance(args, str):
            try:
                json.loads(args)
            except json.JSONDecodeError:
                raise ValueError("Tool call 'arguments' string is not valid JSON")
        elif not isinstance(args, str):
            raise ValueError("Tool call 'arguments' must be a JSON string or a dict")

        return cls(
            id=data["id"],
            type=data.get("type", "function"),
            function=Function(name=func["name"], arguments=args),
        )
