# standard
from unittest.mock import patch
import pytest

# third party
# custom
from sunwaee_gen.providers.anthropic import (
    anthropic_headers_adapter,
    anthropic_messages_adapter,
    anthropic_tools_adapter,
    anthropic_payload_adapter,
)


@pytest.fixture
def anthropic_messages():
    return [
        # NOTE system prompt is in payload
        {
            "role": "user",
            "content": "Hello, how can I help you?",
        },
        {
            "role": "assistant",
            "content": "I need help with coding.",
            "tool_calls": [
                {
                    "id": "call_123",
                    "type": "function",
                    "function": {
                        "name": "search_codebase",
                        "arguments": '{"query": "how to implement authentication"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "content": "Found relevant code in auth.py",
            "tool_call_id": "call_123",
        },
    ]


@pytest.fixture
def anthropic_tools():
    return [
        {
            "name": "search_codebase",
            "description": "Search through the codebase for relevant code snippets",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant code",
                    },
                    "file_type": {
                        "type": "string",
                        "description": "Optional file extension filter (e.g., .py, .js)",
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "analyze_security",
            "description": "Analyze code for security vulnerabilities",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code_path": {
                        "type": "string",
                        "description": "Path to the code to analyze",
                    },
                    "scan_type": {
                        "type": "string",
                        "description": "Type of security scan to perform",
                    },
                },
                "required": ["code_path", "scan_type"],
            },
        },
    ]


class TestAnthropicProvider:

    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    def test_anthropic_headers_adapter_success(self):
        headers = anthropic_headers_adapter()

        expected_headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": "test-key",
        }

        assert headers == expected_headers

    def test_anthropic_headers_adapter_missing_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY is not set"):
            anthropic_headers_adapter()

    def test_anthropic_messages_adapter(
        self, sample_prompt, sample_messages, anthropic_messages
    ):
        adapted_messages = anthropic_messages_adapter(
            system_prompt=sample_prompt,
            messages=sample_messages,
        )
        assert adapted_messages == anthropic_messages

    def test_anthropic_messages_adapter_missing_messages(self, sample_prompt):
        with pytest.raises(ValueError, match="Messages are required"):
            anthropic_messages_adapter(system_prompt=sample_prompt, messages=[])

    def test_anthropic_tools_adapter(self, sample_tools, anthropic_tools):
        adapted_tools = anthropic_tools_adapter(tools=sample_tools)
        assert adapted_tools == anthropic_tools

    def test_anthropic_tools_adapter_missing_tools(self):
        with pytest.raises(ValueError, match="Tools are required"):
            anthropic_tools_adapter()

    def test_anthropic_payload_adapter_full(
        self, sample_prompt, sample_model, sample_messages, anthropic_tools
    ):
        payload = anthropic_payload_adapter(
            model=sample_model,
            system_prompt=sample_prompt,
            messages=sample_messages,
            max_tokens=32000,
            tools=anthropic_tools,
        )

        expected = {
            "model": sample_model,
            "system": sample_prompt,
            "messages": sample_messages,
            "stream": False,
            "max_tokens": 32000,
            "tools": anthropic_tools,
            "thinking": {
                "type": "enabled",
                "budget_tokens": 8192,
            },
        }

        assert payload == expected

    def test_anthropic_payload_adapter_missing_model(
        self, sample_prompt, sample_messages
    ):
        with pytest.raises(ValueError, match="Model is required"):
            anthropic_payload_adapter(
                prompt=sample_prompt,
                messages=sample_messages,
                max_tokens=2048,
            )

    def test_anthropic_payload_adapter_missing_messages(
        self, sample_prompt, sample_model
    ):
        with pytest.raises(ValueError, match="Messages are required"):
            anthropic_payload_adapter(
                model=sample_model,
                prompt=sample_prompt,
                max_tokens=2048,
            )

    def test_anthropic_payload_adapter_missing_max_tokens(
        self, sample_model, sample_prompt, sample_messages
    ):
        with pytest.raises(ValueError, match="Max tokens are required "):
            anthropic_payload_adapter(
                model=sample_model,
                prompt=sample_prompt,
                messages=sample_messages,
            )
