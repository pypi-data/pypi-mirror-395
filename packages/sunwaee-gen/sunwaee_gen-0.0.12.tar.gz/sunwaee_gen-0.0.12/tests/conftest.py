# standard
import pytest

# third party
# custom
from sunwaee_gen.agents.openai import GPT_5_AGENT
from sunwaee_gen.response import Cost, Performance, Response, Usage

agent = GPT_5_AGENT


@pytest.fixture
def sample_prompt():
    return "You are an helpful assistant"


@pytest.fixture
def sample_messages():
    return [
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
def sample_messages_with_system_prompt():
    return [
        {
            "role": "system",
            "content": "You are an helpful assistant.",
        },
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
def sample_tools():
    return [
        {
            "type": "function",
            "function": {
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
        },
        {
            "type": "function",
            "function": {
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
        },
    ]


@pytest.fixture
def sample_api_key():
    return "sk-test-api-key-12345"


@pytest.fixture
def sample_model():
    return "gpt-4"


@pytest.fixture
def sample_agent():
    return GPT_5_AGENT


@pytest.fixture
def sample_provider_config(sample_api_key):
    return {
        "name": "test_provider",
        "url": "https://api.test.com/v1/chat/completions",
        "api_key": sample_api_key,
    }


@pytest.fixture
def empty_stream_chunks():
    return [
        {
            "id": "chatcmpl-empty",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant"},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-empty",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 0,
                "total_tokens": 50,
            },
        },
    ]


@pytest.fixture
def reasoning_and_tools_stream_chunks():
    return [
        {
            "id": "chatcmpl-reasoning-tools",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "reasoning_content": "I need to analyze this request carefully.",
                    },
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-reasoning-tools",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "reasoning_content": " Let me use the appropriate tools for this task."
                    },
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-reasoning-tools",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "tool_calls": [
                            {
                                "id": "call_reasoning123",
                                "type": "function",
                                "function": {
                                    "name": "search_codebase",
                                    "arguments": '{"query": "authentication system"}',
                                },
                            },
                        ]
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        },
        {
            "id": "chatcmpl-reasoning-tools",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "tool_calls": [
                            {
                                "id": "call_reasoning456",
                                "type": "function",
                                "function": {
                                    "name": "analyze_security",
                                    "arguments": '{"code_path": "/src/auth", "scan_type": "full"}',
                                },
                            },
                        ]
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        },
        {
            "id": "chatcmpl-reasoning-tools",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 45,
                "total_tokens": 165,
            },
        },
    ]


@pytest.fixture
def content_only_stream_chunks():
    return [
        {
            "id": "chatcmpl-content-only",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "Here is a simple"},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-content-only",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": " and direct answer"},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-content-only",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": " to your question."},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-content-only",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "gpt-5",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 75,
                "completion_tokens": 15,
                "total_tokens": 90,
            },
        },
    ]


@pytest.fixture
def mocked_response():
    return Response(
        model=agent.model,
        provider=agent.provider,
        reasoning="Let me think about this step by step.",
        content="Here's my response",
        tool_calls=[
            {
                "id": "call_abc123",
                "name": "search_codebase",
                "arguments": {"query": "authentication implementation"},
            },
            {
                "id": "call_def456",
                "name": "analyze_security",
                "arguments": {"code_path": "/src/auth", "scan_type": "vulnerability"},
            },
        ],
        raw='<think>Let me think about this step by step.</think>Here\'s my response<tool_call>{"id": "call_abc123", "name": "search_codebase", "arguments": {"query": "authentication implementation"}}</tool_call><tool_call>{"id": "call_def456", "name": "analyze_security", "arguments": {"code_path": "/src/auth", "scan_type": "vulnerability"}}</tool_call>',
        usage=Usage(prompt_tokens=150, completion_tokens=200, total_tokens=350),
        cost=Cost(
            prompt_cost=150 * agent.cost.input_per_token,
            completion_cost=200 * agent.cost.output_per_token,
            total_cost=150 * agent.cost.input_per_token
            + 200 * agent.cost.output_per_token,
        ),
        performance=Performance(
            latency=0.5,
            reasoning_duration=0.2,
            content_duration=0.3,
            total_duration=0.5,
            throughput=100,
        ),
    ).model_dump()


@pytest.fixture
def mocked_stream():
    return [
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            reasoning="Let me think about this",
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            reasoning=" step by step.",
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            content="Here's my response",
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            tool_calls=[
                {
                    "arguments": {
                        "query": "auth",
                    },
                    "id": "call_abc123",
                    "name": "search_codebase",
                },
            ],
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            tool_calls=[
                {
                    "arguments": {
                        "code_path": "/src/auth",
                        "scan_type": "vulnerability",
                    },
                    "id": "call_def456",
                    "name": "analyze_security",
                },
            ],
        ).model_dump(),
        Response(
            model=agent.model,
            provider=agent.provider,
            streaming=True,
            raw='<think>Let me think about this step by step.</think>Here\'s my response<tool_call>{"id": "call_abc123", "name": "search_codebase", "arguments": {"query": "auth"}}</tool_call><tool_call>{"id": "call_def456", "name": "analyze_security", "arguments": {"code_path": "/src/auth", "scan_type": "vulnerability"}}</tool_call>',
            usage=Usage(prompt_tokens=150, completion_tokens=200, total_tokens=350),
            cost=Cost(
                prompt_cost=150 * agent.cost.input_per_token,
                completion_cost=200 * agent.cost.output_per_token,
                total_cost=150 * agent.cost.input_per_token
                + 200 * agent.cost.output_per_token,
            ),
            performance=Performance(
                latency=0.5,
                reasoning_duration=0.2,
                content_duration=0.3,
                total_duration=0.5,
                throughput=100,
            ),
        ).model_dump(),
    ]
