# standard
import json
import pytest
from unittest.mock import AsyncMock, patch

# third party
# custom
from sunwaee_gen.agents.google import GEMINI_2_5_FLASH_AGENT
from sunwaee_gen.response import Cost, Error, Response, Usage

agent = GEMINI_2_5_FLASH_AGENT


@pytest.fixture
def sample_google_response():
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "reasoning": "Let me think about this step by step.",
                        },
                        {
                            "text": "Here's my response",
                        },
                        {
                            "functionCall": {
                                "name": "search_codebase",
                                "args": {"query": "authentication implementation"},
                            }
                        },
                        {
                            "functionCall": {
                                "name": "analyze_security",
                                "args": {
                                    "code_path": "/src/auth",
                                    "scan_type": "vulnerability",
                                },
                            }
                        },
                    ],
                    "role": "model",
                },
                "finishReason": "STOP",
                "index": 0,
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 150,
            "candidatesTokenCount": 200,
            "totalTokenCount": 350,
        },
        "modelVersion": "gemini-2.5-flash",
    }


@pytest.fixture
def sample_google_stream_chunks():
    # NOTE no reasoning access for google models
    return [
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "reasoning": "Let me think about this",
                            }
                        ],
                        "role": "model",
                    },
                    "index": 0,
                }
            ]
        },
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "reasoning": " step by step.",
                            }
                        ],
                        "role": "model",
                    },
                    "index": 0,
                }
            ]
        },
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Here's my response",
                            }
                        ],
                        "role": "model",
                    },
                    "index": 0,
                }
            ]
        },
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "functionCall": {
                                    "name": "search_codebase",
                                    "args": {
                                        "query": "authentication implementation",
                                    },
                                }
                            }
                        ],
                        "role": "model",
                    },
                    "index": 0,
                }
            ]
        },
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "functionCall": {
                                    "name": "analyze_security",
                                    "args": {
                                        "code_path": "/src/auth",
                                        "scan_type": "vulnerability",
                                    },
                                }
                            }
                        ],
                        "role": "model",
                    },
                    "finishReason": "STOP",
                    "index": 0,
                }
            ]
        },
        {
            "candidates": [
                {
                    "content": {"parts": [], "role": "model"},
                    "finishReason": "STOP",
                    "index": 0,
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 150,
                "candidatesTokenCount": 200,
                "totalTokenCount": 350,
            },
        },
    ]


class TestGoogleAgents:

    @pytest.mark.asyncio
    @patch.dict("os.environ", {}, clear=True)
    async def test_async_completion_missing_api_key(
        self, sample_messages_with_system_prompt
    ):
        with pytest.raises(ValueError, match="GOOGLE_API_KEY is not set"):
            async for _ in agent.async_completion(sample_messages_with_system_prompt):
                break

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_non_streaming_success(
        self,
        mock_post,
        sample_google_response,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_google_response)

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
            usage=Usage(prompt_tokens=150, completion_tokens=200, total_tokens=350),
            cost=Cost(
                prompt_cost=150 * agent.cost.input_per_token,
                completion_cost=200 * agent.cost.output_per_token,
                total_cost=150 * agent.cost.input_per_token
                + 200 * agent.cost.output_per_token,
            ),
        ).model_dump(exclude={"performance", "tool_calls", "raw"})

        assert len(blocks) == 1

        for key, value in expected.items():
            assert blocks[0][key] == value

        assert blocks[0]["raw"].startswith(
            "<think>Let me think about this step by step.</think>Here's my response<tool_call>"
        )

        # NOTE ids are generated at random so assert line by line
        assert isinstance(blocks[0]["tool_calls"][0]["id"], str)
        assert blocks[0]["tool_calls"][0]["name"] == "search_codebase"
        assert blocks[0]["tool_calls"][0]["arguments"] == {
            "query": "authentication implementation"
        }

        assert isinstance(blocks[0]["tool_calls"][1]["id"], str)
        assert blocks[0]["tool_calls"][1]["name"] == "analyze_security"
        assert blocks[0]["tool_calls"][1]["arguments"] == {
            "code_path": "/src/auth",
            "scan_type": "vulnerability",
        }

        assert blocks[0]["performance"]["latency"] >= 0
        assert blocks[0]["performance"]["reasoning_duration"] >= 0
        assert blocks[0]["performance"]["content_duration"] >= 0
        assert blocks[0]["performance"]["total_duration"] >= 0
        assert blocks[0]["performance"]["throughput"] >= 0

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
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
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_success(
        self,
        mock_post,
        sample_google_stream_chunks,
        sample_messages_with_system_prompt,
        sample_tools,
    ):
        sse_lines = []
        for chunk in sample_google_stream_chunks:
            chunk_as_splitted_str = json.dumps(chunk, indent=2).split("\n")
            for sc in chunk_as_splitted_str:
                sse_lines.append(sc.encode("utf-8"))
            sse_lines.append(",\n".encode("utf-8"))
        sse_lines.append("]".encode("utf-8"))
        sse_lines[0] = "[{\n".encode("utf-8")

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
                reasoning="reasoning started, but reasoning tokens are not avaiable for this model...",
            ).model_dump(),
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
            ).model_dump(exclude={"tool_calls"}),
            Response(
                model=agent.model,
                provider=agent.provider,
                streaming=True,
            ).model_dump(exclude={"tool_calls"}),
            Response(
                model=agent.model,
                provider=agent.provider,
                streaming=True,
                usage=Usage(prompt_tokens=150, completion_tokens=200, total_tokens=350),
                cost=Cost(
                    prompt_cost=150 * agent.cost.input_per_token,
                    completion_cost=200 * agent.cost.output_per_token,
                    total_cost=150 * agent.cost.input_per_token
                    + 200 * agent.cost.output_per_token,
                ),
            ).model_dump(exclude={"tool_calls", "performance", "raw"}),
        ]

        assert len(blocks) == len(expected)

        # NOTE first, all but the last 3 blocks
        assert blocks[:-3] == expected[:-3]

        # NOTE last block varies
        for key, value in expected[-1].items():
            assert blocks[-1][key] == value

        assert blocks[-1]["raw"].startswith(
            "<think>Let me think about this step by step.</think>Here's my response<tool_call>"
        )

        # NOTE ids are generated at random so assert line by line
        assert isinstance(blocks[-3]["tool_calls"][0]["id"], str)
        assert blocks[-3]["tool_calls"][0]["name"] == "search_codebase"
        assert blocks[-3]["tool_calls"][0]["arguments"] == {
            "query": "authentication implementation"
        }

        assert isinstance(blocks[-2]["tool_calls"][0]["id"], str)
        assert blocks[-2]["tool_calls"][0]["name"] == "analyze_security"
        assert blocks[-2]["tool_calls"][0]["arguments"] == {
            "code_path": "/src/auth",
            "scan_type": "vulnerability",
        }

        assert blocks[-1]["performance"]["latency"] >= 0
        assert blocks[-1]["performance"]["reasoning_duration"] >= 0
        assert blocks[-1]["performance"]["content_duration"] >= 0
        assert blocks[-1]["performance"]["total_duration"] >= 0
        assert blocks[-1]["performance"]["throughput"] >= 0

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    @patch("aiohttp.ClientSession.post")
    async def test_async_completion_streaming_error(
        self, mock_post, sample_messages_with_system_prompt
    ):
        error_chunk = {
            "error": {
                "code": 429,
                "message": "Quota exceeded for requests per minute per model",
                "status": "RESOURCE_EXHAUSTED",
            }
        }

        sse_lines = []
        sse_lines.append("[{\n".encode("utf-8"))
        chunk_json = json.dumps(error_chunk, indent=2)
        sse_lines.append(chunk_json.encode("utf-8"))
        sse_lines.append("\n]\n".encode("utf-8"))

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
