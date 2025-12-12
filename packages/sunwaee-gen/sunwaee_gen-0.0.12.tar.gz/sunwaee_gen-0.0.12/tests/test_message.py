# standard
import json

# third party
import pytest

# custom
from sunwaee_gen.message import Message


@pytest.fixture
def sample_message_user():
    return {"role": "user", "content": "hi there"}


@pytest.fixture
def sample_message_user_invalid():
    return {"role": "user"}


@pytest.fixture
def sample_message_assistant():
    return {"role": "assistant", "content": "This is the response."}


@pytest.fixture
def sample_message_system():
    return {"role": "system", "content": "You are a helpful assistant."}


@pytest.fixture
def sample_message_tool_call():
    return {
        "role": "assistant",
        "content": "Here's a tool call.",
        "tool_calls": [
            {
                "id": "tc_123",
                "type": "function",
                "function": {
                    "name": "search_codebase",
                    "arguments": '{"query": "auth implementation"}',
                },
            }
        ],
    }


@pytest.fixture
def sample_message_tool_call_invalid():
    return {
        "role": "assistant",
        "content": "some tc",
        "tool_calls": "some tool calls",
    }


@pytest.fixture
def sample_message_tool_result():
    return {
        "role": "tool",
        "content": "Result: 3",
        "tool_call_id": "tc_123",
    }


class TestMessage:

    def test_message_from_dict_user(self, sample_message_user):
        v_message = Message.from_dict(sample_message_user)
        assert v_message.role == "user"
        assert v_message.content == "hi there"

    def test_message_from_dict_assistant(self, sample_message_assistant):
        v_message = Message.from_dict(sample_message_assistant)
        assert v_message.role == "assistant"
        assert v_message.content == "This is the response."

    def test_message_from_dict_system(self, sample_message_system):
        v_message = Message.from_dict(sample_message_system)
        assert v_message.role == "system"
        assert v_message.content == "You are a helpful assistant."

    def test_message_from_dict_tc(self, sample_message_tool_call):
        v_message = Message.from_dict(sample_message_tool_call)
        assert v_message.role == "assistant"
        assert v_message.content == "Here's a tool call."
        assert v_message.tool_calls and len(v_message.tool_calls) == 1
        assert (
            v_message.tool_calls[0].model_dump()
            == sample_message_tool_call["tool_calls"][0]
        )

    def test_message_from_dict_tool_result(self, sample_message_tool_result):
        v_message = Message.from_dict(sample_message_tool_result)
        assert v_message.role == "tool"
        assert v_message.content == "Result: 3"
        assert v_message.tool_call_id == "tc_123"

    def test_message_from_dict_missing_content(self, sample_message_user_invalid):
        with pytest.raises(ValueError, match="Message requires 'role' and 'content'"):
            Message.from_dict(sample_message_user_invalid)

    def test_message_from_dict_invalid_tc(self, sample_message_tool_call_invalid):
        with pytest.raises(ValueError, match="'tool_calls' must be a list of dicts"):
            Message.from_dict(sample_message_tool_call_invalid)

    def test_message_from_list(self, sample_messages_with_system_prompt):
        v_messages = Message.from_list(sample_messages_with_system_prompt)
        assert len(v_messages) == 4
        assert v_messages[0].role == "system"
        assert v_messages[1].role == "user"
        assert v_messages[2].role == "assistant"
        assert v_messages[3].role == "tool"

    def test_message_to_dict_tool_call(self, sample_message_tool_call):
        v_message = Message.from_dict(sample_message_tool_call)
        assert v_message.to_dict() == sample_message_tool_call

    def test_message_to_dict_tool_result(self, sample_message_tool_result):
        v_message = Message.from_dict(sample_message_tool_result)
        assert v_message.to_dict() == sample_message_tool_result

    def test_message_to_str(self, sample_message_tool_call):
        v_message = Message.from_dict(sample_message_tool_call)
        assert str(v_message) == json.dumps(sample_message_tool_call, default=str)
