# standard
import json
import pytest
from unittest.mock import AsyncMock, patch

# third party
# custom
from sunwaee_gen.agents.deepseek import DEEPSEEK_REASONER_AGENT
from sunwaee_gen.response import Cost, Error, Response, Usage

agent = DEEPSEEK_REASONER_AGENT


@pytest.fixture
def sample_deepseek_response():
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1700000000,
        "model": "deepseek-reasoner",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "reasoning_content": "Let me think about this step by step.",
                    "content": "Here's my response",
                    "tool_calls": [
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "search_codebase",
                                "arguments": {"query": "authentication implementation"},
                            },
                        },
                        {
                            "id": "call_def456",
                            "type": "function",
                            "function": {
                                "name": "analyze_security",
                                "arguments": {
                                    "code_path": "/src/auth",
                                    "scan_type": "vulnerability",
                                },
                            },
                        },
                    ],
                },
                "finish_reason": "tool_calls",
            }
        ],
        "usage": {"prompt_tokens": 150, "completion_tokens": 200, "total_tokens": 350},
    }


@pytest.fixture
def sample_deepseek_stream_chunks():
    return [
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "reasoning_content": "Let me think about this",
                    },
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [
                {
                    "index": 0,
                    "delta": {"reasoning_content": " step by step."},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": "Here's my response"},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "tool_calls": [
                            {
                                "id": "call_abc123",
                                "type": "function",
                                "function": {
                                    "name": "search_codebase",
                                    "arguments": '{"query": "authentication implementation"}',
                                },
                            },
                        ]
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "tool_calls": [
                            {
                                "id": "call_def456",
                                "type": "function",
                                "function": {
                                    "name": "analyze_security",
                                    "arguments": '{"code_path": "/src/auth", "scan_type": "vulnerability"}',
                                },
                            },
                        ]
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1700000000,
            "model": "deepseek-reasoner",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 150,
                "completion_tokens": 200,
                "total_tokens": 350,
            },
        },
    ]


class TestDeepSeekAgents:

    @pytest.mark.asyncio
    @patch.dict("os.environ", {}, clear=True)
    async def test_async_completion_missing_api_key(
        self, sample_messages_with_system_prompt
    ):
        with pytest.raises(ValueError, match="DEEPSEEK_API_KEY is not set"):
            async for _ in agent.async_completion(sample_messages_with_system_prompt):
                break

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_non_streaming_success(
        self,
        mock_post,
        sample_deepseek_response,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_deepseek_response)

        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_post.return_value = mock_context

        blocks = []
        async for block in agent.async_completion(
            sample_messages_with_system_prompt, tools=sample_tools, streaming=False
        ):
            blocks.append(block)

        expected = Response(
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
                    "arguments": {
                        "code_path": "/src/auth",
                        "scan_type": "vulnerability",
                    },
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
        ).model_dump(exclude={"performance"})

        assert len(blocks) == 1

        for key, value in expected.items():
            assert blocks[0][key] == value

        assert blocks[0]["performance"]["latency"] >= 0
        assert blocks[0]["performance"]["reasoning_duration"] >= 0
        assert blocks[0]["performance"]["content_duration"] >= 0
        assert blocks[0]["performance"]["total_duration"] >= 0
        assert blocks[0]["performance"]["throughput"] >= 0

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_non_streaming_error(
        self, mock_post, sample_messages_with_system_prompt
    ):
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.text = AsyncMock(return_value="Bad Request: Invalid model")

        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_post.return_value = mock_context

        blocks = []
        async for block in agent.async_completion(
            sample_messages_with_system_prompt, streaming=False
        ):
            blocks.append(block)

        expected = Response(
            model=agent.model,
            provider=agent.provider,
            error=Error(status=400, message="Bad Request: Invalid model"),
        )

        assert len(blocks) == 1
        assert blocks[0] == expected.model_dump()

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_success(
        self,
        mock_post,
        sample_deepseek_stream_chunks,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        sse_lines = []
        for chunk in sample_deepseek_stream_chunks:
            sse_line = f"data: {json.dumps(chunk)}\n".encode("utf-8")
            sse_lines.append(sse_line)

        class MockContent:
            def __init__(self, lines):
                self.lines = lines
                self.index = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content = MockContent(sse_lines)

        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_post.return_value = mock_context

        blocks = []
        async for block in agent.async_completion(
            sample_messages_with_system_prompt, tools=sample_tools, streaming=True
        ):
            blocks.append(block)

        expected = [
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
                            "query": "authentication implementation",
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
                raw='<think>Let me think about this step by step.</think>Here\'s my response<tool_call>{"id": "call_abc123", "name": "search_codebase", "arguments": {"query": "authentication implementation"}}</tool_call><tool_call>{"id": "call_def456", "name": "analyze_security", "arguments": {"code_path": "/src/auth", "scan_type": "vulnerability"}}</tool_call>',
                usage=Usage(prompt_tokens=150, completion_tokens=200, total_tokens=350),
                cost=Cost(
                    prompt_cost=150 * agent.cost.input_per_token,
                    completion_cost=200 * agent.cost.output_per_token,
                    total_cost=150 * agent.cost.input_per_token
                    + 200 * agent.cost.output_per_token,
                ),
            ).model_dump(exclude={"performance"}),
        ]

        assert len(blocks) == len(expected)

        # NOTE first, all but the last block
        assert blocks[:-1] == expected[:-1]

        # NOTE last block varies
        for key, value in expected[-1].items():
            assert blocks[-1][key] == value
        assert blocks[-1]["performance"]["latency"] >= 0
        assert blocks[-1]["performance"]["reasoning_duration"] >= 0
        assert blocks[-1]["performance"]["content_duration"] >= 0
        assert blocks[-1]["performance"]["total_duration"] >= 0
        assert blocks[-1]["performance"]["throughput"] >= 0

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_error(
        self, mock_post, sample_messages_with_system_prompt
    ):
        error_chunk = {
            "error": {
                "type": "invalid_request_error",
                "message": "The model specified does not exist",
                "code": "model_not_found",
            }
        }

        sse_lines = [f"data: {json.dumps(error_chunk)}\n".encode("utf-8")]

        class MockContent:
            def __init__(self, lines):
                self.lines = lines
                self.index = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content = MockContent(sse_lines)

        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_post.return_value = mock_context

        blocks = []
        async for block in agent.async_completion(
            sample_messages_with_system_prompt, streaming=True
        ):
            blocks.append(block)

        # TODO
