# standard
import json
import pytest
from unittest.mock import AsyncMock, patch

# third party
# custom
from sunwaee_gen.agents.anthropic import CLAUDE_4_SONNET_AGENT
from sunwaee_gen.response import Cost, Error, Response, Usage

agent = CLAUDE_4_SONNET_AGENT


@pytest.fixture
def sample_anthropic_response():
    return {
        "id": "msg_123",
        "type": "message",
        "role": "assistant",
        "content": [
            {"type": "thinking", "thinking": "Let me think about this step by step."},
            {"type": "text", "text": "Here's my response"},
            {
                "type": "tool_use",
                "id": "call_abc123",
                "name": "search_codebase",
                "input": {"query": "authentication implementation"},
            },
            {
                "type": "tool_use",
                "id": "call_def456",
                "name": "analyze_security",
                "input": {"code_path": "/src/auth", "scan_type": "vulnerability"},
            },
        ],
        "model": "claude-3-5-sonnet-20241022",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 150, "output_tokens": 200},
    }


@pytest.fixture
def sample_anthropic_stream():
    return [
        {
            "type": "message_start",
            "message": {
                "id": "msg_123",
                "type": "message",
                "role": "assistant",
                "content": [],
                "model": "claude-3-5-sonnet-20241022",
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 150, "output_tokens": 0},
            },
        },
        {
            "type": "content_block_start",
            "index": 0,
            "content_block": {"type": "thinking", "thinking": ""},
        },
        {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "thinking_delta", "thinking": "Let me think about this"},
        },
        {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "thinking_delta", "thinking": " step by step."},
        },
        {"type": "content_block_stop", "index": 0},
        {
            "type": "content_block_start",
            "index": 1,
            "content_block": {"type": "text", "text": ""},
        },
        {
            "type": "content_block_delta",
            "index": 1,
            "delta": {"type": "text_delta", "text": "Here's my response"},
        },
        {"type": "content_block_stop", "index": 1},
        {
            "type": "content_block_start",
            "index": 2,
            "content_block": {
                "type": "tool_use",
                "id": "call_abc123",
                "name": "search_codebase",
                "input": {},
            },
        },
        {
            "type": "content_block_delta",
            "index": 2,
            "delta": {
                "type": "input_json_delta",
                "partial_json": '{"query": "authentication implementation"}',
            },
        },
        {"type": "content_block_stop", "index": 2},
        {
            "type": "content_block_start",
            "index": 3,
            "content_block": {
                "type": "tool_use",
                "id": "call_def456",
                "name": "analyze_security",
                "input": {},
            },
        },
        {
            "type": "content_block_delta",
            "index": 3,
            "delta": {
                "type": "input_json_delta",
                "partial_json": '{"code_path": "/src/auth", "scan_type": "vulnerability"}',
            },
        },
        {"type": "content_block_stop", "index": 3},
        {
            "type": "message_delta",
            "delta": {"stop_reason": "end_turn"},
            "usage": {"output_tokens": 200},
            "message": {"usage": {"input_tokens": 150, "output_tokens": 200}},
        },
        {"type": "message_stop"},
    ]


class TestAnthropicAgents:

    @pytest.mark.asyncio
    @patch.dict("os.environ", {}, clear=True)
    async def test_async_completion_missing_api_key(
        self, sample_messages_with_system_prompt
    ):
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY is not set"):
            async for _ in agent.async_completion(sample_messages_with_system_prompt):
                pass

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_non_streaming_success(
        self,
        mock_post,
        sample_anthropic_response,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_anthropic_response)

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
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
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
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_success(
        self,
        mock_post,
        sample_anthropic_stream,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        sse_lines = []
        for chunk in sample_anthropic_stream:
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
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_error(
        self, mock_post, sample_messages_with_system_prompt
    ):
        error_chunk = {
            "type": "error",
            "error": {
                "type": "invalid_request_error",
                "message": "Invalid model specified",
            },
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
