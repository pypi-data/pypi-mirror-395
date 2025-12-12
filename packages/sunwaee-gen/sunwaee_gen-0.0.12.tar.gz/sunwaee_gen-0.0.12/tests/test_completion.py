# standard
import pytest
from unittest.mock import patch

# third party
# custom
from sunwaee_gen import async_completion
from sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from sunwaee_gen.model import Model
from sunwaee_gen.provider import Provider


class TestGenCompletion:

    @pytest.mark.asyncio
    async def test_async_completion_invalid_agent_name(
        self, sample_messages, sample_tools
    ):
        with pytest.raises(ValueError) as exc_info:
            async for _ in async_completion(
                agent="invalid/agent-name",
                messages=sample_messages,
                tools=sample_tools,
            ):
                pass

        error_message = str(exc_info.value)
        assert "Agent 'invalid/agent-name' not found" in error_message
        assert "Available agents:" in error_message

    @pytest.mark.asyncio
    async def test_async_completion_non_streaming_success(
        self, sample_agent, sample_messages, sample_tools, mocked_response
    ):

        async def mock_async_generator():
            yield mocked_response

        with patch.object(sample_agent, "async_completion") as mock_agent_completion:

            mock_agent_completion.return_value = mock_async_generator()

            blocks = []
            async for block in async_completion(
                sample_agent.name,
                messages=sample_messages,
                tools=sample_tools,
                streaming=False,
            ):
                blocks.append(block)

            assert len(blocks) == 1
            assert blocks[0] == mocked_response

    @pytest.mark.asyncio
    async def test_async_completion_streaming_success(
        self, sample_agent, sample_messages, sample_tools, mocked_stream
    ):

        async def mock_async_generator():
            for block in mocked_stream:
                yield block

        with patch.object(sample_agent, "async_completion") as mock_agent_completion:

            mock_agent_completion.return_value = mock_async_generator()

            blocks = []
            async for block in async_completion(
                sample_agent.name,
                messages=sample_messages,
                tools=sample_tools,
                streaming=True,
            ):
                blocks.append(block)

            assert len(blocks) == len(mocked_stream)
            assert blocks == mocked_stream

    @pytest.mark.asyncio
    async def test_async_completion_with_agent_object(
        self, sample_agent, sample_messages, sample_tools, mocked_response
    ):

        async def mock_async_generator():
            yield mocked_response

        with patch.object(sample_agent, "async_completion") as mock_agent_completion:

            mock_agent_completion.return_value = mock_async_generator()

            blocks = []
            async for block in async_completion(
                sample_agent,
                messages=sample_messages,
                tools=sample_tools,
                streaming=False,
            ):
                blocks.append(block)

            assert len(blocks) == 1
            assert blocks[0] == mocked_response

    @pytest.mark.asyncio
    async def test_async_completion_with_custom_agent(
        self, sample_messages, sample_tools, mocked_response
    ):
        custom_model = Model(
            name="test-model",
            display_name="Test Model",
            origin="test",
        )
        custom_provider = Provider(
            name="test",
            url="https://api.test.com/v1/chat/completions",
        )
        custom_agent = Agent(
            name="test/test-model",
            model=custom_model,
            provider=custom_provider,
            cost=AgentCost(input_per_1m_token=1.0, output_per_1m_token=2.0),
            specs=AgentSpecs(max_input_tokens=1000, max_output_tokens=500),
            features=AgentFeatures(),
        )

        async def mock_async_generator():
            yield mocked_response

        with patch.object(custom_agent, "async_completion") as mock_custom_completion:

            mock_custom_completion.return_value = mock_async_generator()

            blocks = []
            async for block in async_completion(
                custom_agent,
                messages=sample_messages,
                tools=sample_tools,
            ):
                blocks.append(block)

            assert len(blocks) == 1
            assert blocks[0] == mocked_response
