# standard
import os
import typing

# third party
import pydantic

# custom


def default_headers_adapter(**kwargs) -> dict:
    """
    {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    """

    provider = kwargs.get("provider")
    if not provider:
        raise ValueError("Provider is required for default headers adapter")

    api_key = kwargs.get("api_key") or os.getenv(f"{provider.upper()}_API_KEY")
    if not api_key:
        raise ValueError(f"{provider.upper()}_API_KEY is not set")

    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def default_messages_adapter(**kwargs) -> list[dict]:
    """
    [
        # --- MESSAGE
        {
            "role": str,
            "content": str,
        }
        # --- TOOL CALL
        {
            "role": str,
            "content": str,
            "tool_calls": [
                {
                    "id": str,
                    "type": str,
                    "function": {
                        "name": str,
                        "arguments": str,
                    },
                }
            ],
        }
        # --- TOOL CALL RESULT
        {
            "role": str,
            "content": str,
            "tool_call_id": str,
        }
    ]
    """

    if not kwargs.get("messages"):
        raise ValueError("Messages are required for default messages adapter")

    if system_prompt := kwargs.get("system_prompt"):
        kwargs["messages"] = [
            {"role": "system", "content": system_prompt},
            *kwargs.get("messages", []),
        ]

    return kwargs.get("messages", [])


def default_tools_adapter(**kwargs) -> list[dict]:
    """
    [
        {
            "type": "function",
            "function": {
                "name": str,
                "description": str,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "property1": {
                            "type": "string",
                            "description": "Description of property1",
                        },
                        "property2": {
                            "type": "number",
                            "description": "Description of property2",
                        },
                    },
                    "required": ["property1", "property2"],
                },
            },
        }
    ]
    """

    if not kwargs.get("tools"):
        raise ValueError("Tools are required for default tools adapter")

    return kwargs.get("tools", [])


def default_payload_adapter(**kwargs) -> dict:
    """
    {
        "model": str,
        "messages": list[dict],
        "stream": bool,
        "tools": list[dict], # only if tools are supported
        "stream_options": {
            "include_usage": True, # only if streaming is supported
        },
    }
    """

    if not kwargs.get("model"):
        raise ValueError("Model is required for default payload adapter")
    if not kwargs.get("messages"):
        raise ValueError("Messages are required for default payload adapter")

    if not kwargs.get("streaming"):
        kwargs["streaming"] = False

    if prompt := kwargs.get("system_prompt"):
        kwargs["messages"] = [
            {"role": "system", "content": prompt},
            *kwargs.get("messages", [{}]),
        ]

    payload = {
        "model": kwargs.get("model"),
        "messages": kwargs.get("messages"),
        "stream": kwargs.get("streaming"),
    }

    if tools := kwargs.get("tools"):
        payload["tools"] = tools

    if kwargs.get("streaming"):
        payload["stream_options"] = {"include_usage": True}

    return payload


def default_sse_adapter() -> dict:
    """
    {
        "content": str, # path to response content
        "reasoning": str, # path to response reasoning_content
        "tool_call_id": str, # path to response tool call id
        "tool_call_name": str, # path to response tool call name
        "tool_call_arguments": str, # path to response tool call arguments
        "prompt_tokens": str, # path to response prompt tokens
        "completion_tokens": str, # path to response completion tokens
        "total_tokens": str, # path to response total tokens
    }
    """

    return {
        "content": "choices.0.delta.content",
        "reasoning": "choices.0.delta.reasoning_content",
        "tool_call_id": "choices.0.delta.tool_calls.[function].id",
        "tool_call_name": "choices.0.delta.tool_calls.[function].function.[name].name",
        "tool_call_arguments": "choices.0.delta.tool_calls.[function].function.[arguments].arguments",
        "prompt_tokens": "usage.prompt_tokens",
        "completion_tokens": "usage.completion_tokens",
        "total_tokens": "usage.total_tokens",
    }


def default_response_adapter() -> dict:
    """
    {
        "content": str, # path to response content
        "reasoning": str, # path to response reasoning_content
        "tool_calls": str, # path to response tool calls array
        "tool_call_id": str, # path to response tool call id (relative to tool_call)
        "tool_call_name": str, # path to response tool call name (relative to tool_call)
        "tool_call_arguments": str, # path to response tool call arguments (relative to tool_call)
        "prompt_tokens": str, # path to response prompt tokens
        "completion_tokens": str, # path to response completion tokens
        "total_tokens": str, # path to response total tokens
    }
    """

    return {
        "content": "choices.0.message.content",
        "reasoning": "choices.0.message.reasoning_content",
        "tool_call_id": "choices.0.message.tool_calls.[function].id",
        "tool_call_name": "choices.0.message.tool_calls.[function].function.[name].name",
        "tool_call_arguments": "choices.0.message.tool_calls.[function].function.[arguments].arguments",
        "prompt_tokens": "usage.prompt_tokens",
        "completion_tokens": "usage.completion_tokens",
        "total_tokens": "usage.total_tokens",
    }


class Provider(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    name: str
    url: str

    headers_adapter: typing.Callable[..., dict] = pydantic.Field(
        default_factory=lambda: default_headers_adapter,
        repr=False,
        exclude=True,
    )
    payload_adapter: typing.Callable[..., dict] = pydantic.Field(
        default_factory=lambda: default_payload_adapter,
        repr=False,
        exclude=True,
    )
    messages_adapter: typing.Callable[..., list[dict]] = pydantic.Field(
        default_factory=lambda: default_messages_adapter,
        repr=False,
        exclude=True,
    )
    tools_adapter: typing.Callable[..., list[dict]] = pydantic.Field(
        default_factory=lambda: default_tools_adapter,
        repr=False,
        exclude=True,
    )
    sse_adapter: typing.Callable[[], dict] = pydantic.Field(
        default_factory=lambda: default_sse_adapter,
        repr=False,
        exclude=True,
    )
    response_adapter: typing.Callable[[], dict] = pydantic.Field(
        default_factory=lambda: default_response_adapter,
        repr=False,
        exclude=True,
    )
