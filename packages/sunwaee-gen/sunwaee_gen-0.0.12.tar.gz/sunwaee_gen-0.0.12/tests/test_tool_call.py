# standard
# third party
import pytest

# custom
from sunwaee_gen.tool_call import ToolCall


@pytest.fixture
def sample_tool_call():
    return {
        "id": "tc_123",
        "type": "function",
        "function": {
            "name": "get_weather",
            "arguments": '{"city": "Paris"}',
        },
    }


class TestToolCall:

    def test_tool_call_from_dict(self, sample_tool_call):
        tool_call = ToolCall.from_dict(sample_tool_call)
        assert tool_call.id == sample_tool_call["id"]
        assert tool_call.type == sample_tool_call["type"]
        assert tool_call.function.name == sample_tool_call["function"]["name"]
        assert tool_call.function.arguments == sample_tool_call["function"]["arguments"]

    def test_tool_call_from_dict_missing_id(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv.pop("id")

        with pytest.raises(ValueError, match="requires a non-empty 'id'"):
            ToolCall.from_dict(inv)

    def test_tool_call_from_dict_missing_function(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv.pop("function")

        with pytest.raises(ValueError, match="requires a 'function' object"):
            ToolCall.from_dict(inv)

    def test_tool_call_from_dict_missing(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv["function"].pop("name")

        with pytest.raises(ValueError, match="requires a non-empty 'name'"):
            ToolCall.from_dict(inv)

    def test_tool_call_from_dict_missing_arguments(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv["function"].pop("arguments")

        with pytest.raises(ValueError, match="requires 'arguments'"):
            ToolCall.from_dict(inv)

    def test_tool_call_from_dict_invalid_arguments(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv["function"]["arguments"] = ["list", "of", "args"]

        with pytest.raises(ValueError, match="must be a JSON string or a dict"):
            ToolCall.from_dict(inv)

    def test_tool_call_from_dict_invalid_json(self, sample_tool_call):
        inv = sample_tool_call.copy()
        inv["function"]["arguments"] = "invalid json"

        with pytest.raises(ValueError, match="is not valid JSON"):
            ToolCall.from_dict(inv)

    def test_tool_call_to_dict(self, sample_tool_call):
        tool_call = ToolCall.from_dict(sample_tool_call)
        assert tool_call.model_dump() == sample_tool_call
