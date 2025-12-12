# standard
# third party
import pytest

# custom
from sunwaee_gen.provider import (
    default_headers_adapter,
    default_messages_adapter,
    default_tools_adapter,
    default_payload_adapter,
)


class TestProvider:

    def test_provider_default_headers_adapter_missing_provider(self):
        with pytest.raises(ValueError, match="Provider is required"):
            default_headers_adapter()

    def test_provider_default_headers_adapter_missing_key(self):
        with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
            default_headers_adapter(provider="openai")

    def test_provider_default_messages_adapter_missing_messages(self):
        with pytest.raises(ValueError, match="Messages are required"):
            default_messages_adapter()

    def test_provider_default_tools_adapter_missing_tools(self):
        with pytest.raises(ValueError, match="Tools are required"):
            default_tools_adapter()

    def test_provider_default_payload_adapter_missing_model(self, sample_messages):
        with pytest.raises(ValueError, match="Model is required"):
            default_payload_adapter(messages=sample_messages)

    def test_provider_default_payload_adapter_missing_messages(self, sample_model):
        with pytest.raises(ValueError, match="Messages are required"):
            default_payload_adapter(model=sample_model)
