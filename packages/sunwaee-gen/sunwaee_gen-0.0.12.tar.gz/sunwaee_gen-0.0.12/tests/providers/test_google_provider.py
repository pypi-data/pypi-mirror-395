# standard
import pytest
from unittest.mock import patch

# third party
# custom
from sunwaee_gen.providers.google import (
    google_headers_adapter,
    google_messages_adapter,
    google_tools_adapter,
    google_payload_adapter,
)


@pytest.fixture
def google_tools():
    return [
        {
            "functionDeclarations": [
                {
                    "name": "search_codebase",
                    "description": "Search through the codebase for relevant code snippets",
                    "parameters": {
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
                    "parameters": {
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
        }
    ]


@pytest.fixture
def google_messages():
    return [
        {"role": "user", "parts": [{"text": "Hello, how can I help you?"}]},
        {
            "role": "model",
            "parts": [
                {
                    "functionCall": {
                        "name": "search_codebase",
                        "args": {"query": "how to implement authentication"},
                    }
                }
            ],
        },
        {"role": "user", "parts": [{"text": "Found relevant code in auth.py"}]},
    ]


class TestGoogleProvider:

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    def test_google_headers_adapter_success(self):
        headers = google_headers_adapter()

        expected_headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": "test-key",
        }

        assert headers == expected_headers

    def test_google_headers_adapter_missing_key(self):
        with pytest.raises(ValueError, match="GOOGLE_API_KEY is not set"):
            google_headers_adapter()

    def test_google_messages_adapter(
        self, sample_prompt, sample_messages, google_messages
    ):
        adapted_messages = google_messages_adapter(
            system_prompt=sample_prompt,
            messages=sample_messages,
        )
        assert adapted_messages == google_messages

    def test_google_messages_adapter_missing_messages(self):
        with pytest.raises(ValueError, match="Messages are required"):
            google_messages_adapter()

    def test_google_tools_adapter(self, sample_tools, google_tools):
        adapted_tools = google_tools_adapter(tools=sample_tools)
        assert adapted_tools == google_tools

    def test_google_tools_adapter_missing_tools(self):
        with pytest.raises(ValueError, match="Tools are required"):
            google_tools_adapter()

    def test_google_payload_adapter(self, google_messages, google_tools, sample_prompt):
        payload = google_payload_adapter(
            system_prompt=sample_prompt,
            messages=google_messages,
            tools=google_tools,
        )

        expected_payload = {
            "systemInstruction": {"parts": [{"text": sample_prompt}]},
            "contents": google_messages,
            "tools": google_tools,
        }

        assert payload == expected_payload

    def test_google_payload_adapter_missing_messages(self):
        with pytest.raises(ValueError, match="Messages are required"):
            google_payload_adapter()
