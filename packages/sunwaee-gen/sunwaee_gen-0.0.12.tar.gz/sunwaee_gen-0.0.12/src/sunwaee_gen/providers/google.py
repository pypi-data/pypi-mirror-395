# standard
import os
import json

# third party
# custom
from sunwaee_gen.provider import Provider
from sunwaee_gen.helpers import get_nested_dict_value


# --- GOOGLE
# hi there we just want to make your dev experience as painful as possible, you're welcome :)
# P.S. GOOGLE WHAT IS THIS SHIT?????


def google_headers_adapter(**kwargs) -> dict:
    """
    {
        "Content-Type": "application/json",
        "x-goog-api-key": str,
    }
    """

    api_key = kwargs.get("api_key") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")

    return {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }


def google_messages_adapter(**kwargs) -> list[dict]:
    """
    [
        # --- MESSAGE
        {
            "role": literal["assistant", "user"],
            "parts": [
                {
                    "text": str,
                },
            ]
        },
        # --- TOOL CALL
        {
            "role": "assistant",
            "parts": [
                {
                    "functionCall": {
                        "name": str,
                        "args": dict, # yeah fucking JSON obj and not JSON str...
                    },
                }, ...
            ]
        },
        # --- TOOL CALL RESULT
        {
            "role": "tool",
            "tool_call_id": str,
            "content": str,
        }
    ]
    """

    if not kwargs.get("messages"):
        raise ValueError("Messages are required for google messages adapter")

    formatted_messages = []
    for m in kwargs.get("messages", [{}]):
        role = "model" if m["role"] == "assistant" else "user"
        base: dict = {"role": role}
        if c := m.get("content"):
            base["parts"] = [{"text": c}]
        if tool_calls := m.get("tool_calls"):
            base["parts"] = [
                {
                    "functionCall": {
                        "name": tc.get("function", {}).get("name"),
                        "args": json.loads(tc.get("function", {}).get("arguments")),
                    },
                }
                for tc in tool_calls
            ]
        formatted_messages.append(base)

    return formatted_messages


def google_tools_adapter(**kwargs) -> list[dict]:
    """
    format = [
        {
            "functionDeclarations": [
                {
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
                }, ...
            ]
        }
    ]
    """

    if not kwargs.get("tools"):
        raise ValueError("Tools are required for google tools adapter")

    return [
        {
            "functionDeclarations": [
                get_nested_dict_value(t, "function") for t in kwargs.get("tools", [])
            ]
        }
    ]


def google_payload_adapter(**kwargs) -> dict:
    """
    {
        "systemInstruction": {"parts": [{"text": str}]},
        "contents": list[dict], # without system messages
        "tools": list[dict], # only if tools are supported
    }
    """

    if not kwargs.get("messages"):
        raise ValueError("Messages are required for google payload adapter")

    payload = {"contents": kwargs.get("messages")}

    if prompt := kwargs.get("system_prompt"):
        payload["systemInstruction"] = {"parts": [{"text": prompt}]}

    if tools := kwargs.get("tools"):
        payload["tools"] = tools

    return payload


def google_sse_adapter() -> dict:
    """
    {
        "content": str,
        "reasoning": str,
        "tool_call_id": str,
        "tool_call_name": str,
        "tool_call_arguments": str,
        "prompt_tokens": str,
        "completion_tokens": str,
        "total_tokens": str,
    }
    """

    return {
        "content": "candidates.0.content.parts.[text].text",
        "reasoning": "candidates.0.content.parts.[reasoning].reasoning",
        "tool_call_id": "",  # will be generated
        "tool_call_name": "candidates.0.content.parts.[functionCall].functionCall.[name].name",
        "tool_call_arguments": "candidates.0.content.parts.[functionCall].functionCall.[args].args",
        "prompt_tokens": "usageMetadata.promptTokenCount",
        "completion_tokens": "usageMetadata.candidatesTokenCount",
        "total_tokens": "usageMetadata.totalTokenCount",
    }


def google_response_adapter() -> dict:
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
        "content": "candidates.0.content.parts.[text].text",
        "reasoning": "candidates.0.content.parts.[reasoning].reasoning",
        "tool_call_id": "",  # will be generated
        "tool_call_name": "candidates.0.content.parts.[functionCall].functionCall.[name].name",
        "tool_call_arguments": "candidates.0.content.parts.[functionCall].functionCall.[args].args",
        "prompt_tokens": "usageMetadata.promptTokenCount",
        "completion_tokens": "usageMetadata.candidatesTokenCount",
        "total_tokens": "usageMetadata.totalTokenCount",
    }


GOOGLE = Provider(
    name="google",
    url="https://generativelanguage.googleapis.com/v1beta/models/<|model_name|>:<|gen_method|>",  # for real???
    headers_adapter=google_headers_adapter,
    messages_adapter=google_messages_adapter,
    tools_adapter=google_tools_adapter,
    payload_adapter=google_payload_adapter,
    sse_adapter=google_sse_adapter,
    response_adapter=google_response_adapter,
)
