# standard
from unittest.mock import patch

# third party
import httpx
import pytest

# custom
from sunwaee_gen import AGENTS
from sunwaee_gen import MODELS
from sunwaee_gen import PROVIDERS
from sunwaee_gen.api import api


class TestGenAPI:
    @pytest.mark.asyncio
    async def test_list_models(self):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api),
            base_url="http://test",
        ) as ac:
            response = await ac.get("/models")
        assert response.status_code == 200
        assert response.json() == [m.model_dump() for m in MODELS.values()]

    @pytest.mark.asyncio
    async def test_list_providers(self):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api),
            base_url="http://test",
        ) as ac:
            response = await ac.get("/providers")
        assert response.status_code == 200
        assert response.json() == [p.model_dump() for p in PROVIDERS.values()]

    @pytest.mark.asyncio
    async def test_list_agents(self):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api),
            base_url="http://test",
        ) as ac:
            response = await ac.get("/agents")
        assert response.status_code == 200
        assert response.json() == [a.model_dump() for a in AGENTS.values()]

    @pytest.mark.asyncio
    async def test_llm_completion_non_streaming_success(
        self,
        sample_agent,
        sample_messages_with_system_prompt,
        sample_tools,
        mocked_response,
    ):
        async def mock_async_generator(*args, **kwargs):
            yield mocked_response

        with patch.object(sample_agent, "async_completion") as mock_agent_completion:

            mock_agent_completion.return_value = mock_async_generator()

            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=api),
                base_url="http://test",
            ) as ac:
                response = await ac.post(
                    "/completion",
                    headers={"Authorization": "Bearer test-api-key"},
                    json={
                        "agent": sample_agent.name,
                        "messages": sample_messages_with_system_prompt,
                        "tools": sample_tools,
                        "streaming": False,
                    },
                )

            assert response.status_code == 200
            response_data = response.json()

            assert response_data == mocked_response

    @pytest.mark.asyncio
    async def test_llm_completion_non_streaming_error(self):
        pass

    @pytest.mark.asyncio
    async def test_llm_completion_streaming_success(
        self,
        sample_agent,
        sample_messages_with_system_prompt,
        sample_tools,
        mocked_stream,
    ):
        async def mock_async_generator(*args, **kwargs):
            yield mocked_stream

        with patch.object(sample_agent, "async_completion") as mock_agent_completion:

            mock_agent_completion.return_value = mock_async_generator()

            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=api),
                base_url="http://test",
            ) as ac:
                response = await ac.post(
                    "/completion",
                    headers={"Authorization": "Bearer test-api-key"},
                    json={
                        "agent": sample_agent.name,
                        "messages": sample_messages_with_system_prompt,
                        "tools": sample_tools,
                        "streaming": True,
                    },
                )

            assert response.status_code == 200
            response_data = response.json()

            assert response_data == mocked_stream

    @pytest.mark.asyncio
    async def test_llm_completion_streaming_error(self):
        pass

    @pytest.mark.asyncio
    async def test_llm_completion_missing_bearer(
        self, sample_agent, sample_messages_with_system_prompt, sample_tools
    ):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api),
            base_url="http://test",
        ) as ac:
            response = await ac.post(
                "/completion",
                json={
                    "agent": sample_agent.name,
                    "messages": sample_messages_with_system_prompt,
                    "tools": sample_tools,
                    "streaming": True,
                },
            )

            assert response.status_code == 403
