# standard
import os

# third party
# custom
from sunwaee_gen.helpers import get_nested_dict_value
from sunwaee_gen.provider import Provider


# --- ANTHROPIC
# hi there we're the weirdos trying to establish a new standard


def anthropic_headers_adapter(**kwargs) -> dict:
    """
    {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": str,
    }
    """

    api_key = kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set")

    return {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": api_key,
    }


def anthropic_messages_adapter(**kwargs) -> list[dict]:
    # NOTE no system prompt in the messages
    if not kwargs.get("messages"):
        raise ValueError("Messages are required for anthropic messages adapter")

    return kwargs.get("messages", [])


def anthropic_tools_adapter(**kwargs) -> list[dict]:
    """
    [
        {
            "name": str,
            "description": str,
            "input_schema": {
                "type": "object",
                "properties": dict,
                "required": list[str],
            },
        }, ...
    ]
    """

    if not kwargs.get("tools"):
        raise ValueError("Tools are required for anthropic tools adapter")

    return [
        {
            "name": get_nested_dict_value(tool_dict, "function.name"),
            "description": get_nested_dict_value(tool_dict, "function.description"),
            "input_schema": get_nested_dict_value(tool_dict, "function.parameters"),
        }
        for tool_dict in kwargs.get("tools", [])
    ]


def anthropic_payload_adapter(**kwargs) -> dict:
    """
    {
        "model": str,
        "system": str, # extracted from system messages
        "messages": list[dict], # without system messages
        "stream": bool,
        "max_tokens": int, # only if max_tokens is supported
        "tools": list[dict], # only if tools are supported
        "thinking": {
            "type": str, # default is "enabled"
            "budget_tokens": int, # default is 8192
        },
    }
    """

    if not kwargs.get("model"):
        raise ValueError("Model is required for anthropic payload adapter")
    if not kwargs.get("messages"):
        raise ValueError("Messages are required for anthropic payload adapter")
    if not kwargs.get("max_tokens"):
        raise ValueError("Max tokens are required for anthropic payload adapter")

    if not kwargs.get("streaming"):
        kwargs["streaming"] = False
    if not kwargs.get("thinking"):
        kwargs["thinking"] = {
            "type": "enabled",
            "budget_tokens": 8192,
        }

    payload = {
        "model": kwargs.get("model"),
        "max_tokens": kwargs.get("max_tokens"),
        "messages": kwargs.get("messages"),
        "thinking": kwargs.get("thinking"),
        "stream": kwargs.get("streaming"),
    }

    if prompt := kwargs.get("system_prompt"):
        payload["system"] = prompt

    if tools := kwargs.get("tools"):
        payload["tools"] = tools

    return payload


def anthropic_sse_adapter() -> dict:
    """
    {
        "content": str,
        "reasoning": str,
        "tool_call_id": str,
        "tool_call_name": str,
        "tool_call_arguments": str,
        "prompt_tokens": str,
        "completion_tokens": str,
    }
    """

    return {
        "content": "delta.text",
        "reasoning": "delta.thinking",
        "tool_call_id": "content_block.id",
        "tool_call_name": "content_block.name",
        "tool_call_arguments": "delta.partial_json",
        "prompt_tokens": "message.usage.input_tokens",
        "completion_tokens": "message.usage.output_tokens",
        "total_tokens": "",  # will be computed
    }


def anthropic_response_adapter() -> dict:
    """
    {
        "content": str,
        "reasoning": str,
        "tool_calls": str,
        "tool_call_id": str,
        "tool_call_name": str,
        "tool_call_arguments": str,
        "prompt_tokens": str,
        "completion_tokens": str,
        "total_tokens": str,
    }
    """

    return {
        "content": "content.[type=text].text",
        "reasoning": "content.[type=thinking].thinking",
        "tool_call_id": "content.[type=tool_use].id",
        "tool_call_name": "content.[type=tool_use].name",
        "tool_call_arguments": "content.[type=tool_use].input",
        "prompt_tokens": "usage.input_tokens",
        "completion_tokens": "usage.output_tokens",
        "total_tokens": "",  # will be computed
    }


ANTHROPIC = Provider(
    name="anthropic",
    url="https://api.anthropic.com/v1/messages",
    headers_adapter=anthropic_headers_adapter,
    messages_adapter=anthropic_messages_adapter,
    tools_adapter=anthropic_tools_adapter,
    payload_adapter=anthropic_payload_adapter,
    sse_adapter=anthropic_sse_adapter,
    response_adapter=anthropic_response_adapter,
)
