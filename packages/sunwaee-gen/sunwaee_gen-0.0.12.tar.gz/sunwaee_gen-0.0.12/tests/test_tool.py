# standard
# third party
import pytest

# custom
from sunwaee_gen import Tool, T


@pytest.fixture
def sample_tool():
    return {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city (e.g. Paris, London...)",
                    },
                },
                "required": ["city"],
            },
        },
    }


@pytest.fixture
def sample_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city (e.g. Paris, London...)",
                        },
                    },
                    "required": ["city"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_hour",
                "description": "Get hour.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "The timezone (e.g. Paris, London...)",
                        },
                    },
                    "required": ["timezone"],
                },
            },
        },
    ]


class TestTool:

    def test_tool_from_dict(self, sample_tool):
        tool = Tool.from_dict(sample_tool)
        assert tool.type == sample_tool["type"]
        assert tool.function.name == sample_tool["function"]["name"]
        assert tool.function.description == sample_tool["function"]["description"]
        assert (
            tool.function.parameters.properties["city"].model_dump()
            == sample_tool["function"]["parameters"]["properties"]["city"]
        )
        assert (
            tool.function.parameters.required
            == sample_tool["function"]["parameters"]["required"]
        )

    def test_tool_from_dict_missing_prop(self, sample_tool):
        tool = sample_tool.copy()
        tool["function"]["parameters"]["properties"] = {}
        with pytest.raises(ValueError, match="properties must be a non-empty dict"):
            Tool.from_dict(tool)

    def test_tool_from_list(self, sample_tools):
        tools = Tool.from_list(sample_tools)
        assert len(tools) == 2

        for idx, tool in enumerate(tools):
            assert tool.type == sample_tools[idx]["type"]
            assert tool.function.name == sample_tools[idx]["function"]["name"]
            assert (
                tool.function.description
                == sample_tools[idx]["function"]["description"]
            )
            assert (
                tool.function.parameters.model_dump()
                == sample_tools[idx]["function"]["parameters"]
            )
            assert (
                tool.function.parameters.required
                == sample_tools[idx]["function"]["parameters"]["required"]
            )

    def test_tool_decorator_basic(self):
        @T()
        def test_func(param1: str, param2: int = 10) -> str:
            """Test function description.

            param1: Description of param1
            param2: Description of param2"""
            return f"{param1}: {param2}"

        assert isinstance(test_func, Tool)
        assert test_func.function.name == "test_func"
        assert test_func.function.description == "Test function description."
        assert "param1" in test_func.function.parameters.properties
        assert "param2" in test_func.function.parameters.properties
        assert test_func.function.parameters.required == ["param1"]

    def test_tool_decorator_schema(self, sample_tool):
        @T()
        def get_weather(city: str):
            """
            Get weather.

            city: The city (e.g. Paris, London...)
            """
            pass

        assert get_weather.model_dump(mode="json") == sample_tool

    def test_tool_decorator_ignore_params(self):
        @T(ignore=["internal"])
        def test_func(param1: str, internal: str = "secret") -> str:
            """Test function with ignored param.

            param1: Description of param1"""
            return param1

        assert "param1" in test_func.function.parameters.properties
        assert "internal" not in test_func.function.parameters.properties
        assert test_func.function.parameters.required == ["param1"]

    def test_tool_decorator_no_docstring(self):
        @T()
        def test_func(param1: str) -> str:
            return param1

        assert test_func.function.description == "Function test_func"
        assert "param1" in test_func.function.parameters.properties

    def test_t_decorator_parameter_types(self):
        @T()
        def test_func(
            str_param: str,
            int_param: int,
            float_param: float,
            bool_param: bool,
            list_param: list,
            dict_param: dict,
            untyped_param,
        ) -> str:
            """Test function with various parameter types.

            str_param: String parameter
            int_param: Integer parameter
            float_param: Float parameter
            bool_param: Boolean parameter
            list_param: List parameter
            dict_param: Dictionary parameter
            untyped_param: Untyped parameter"""
            return "test"

        properties = test_func.function.parameters.properties

        assert properties["str_param"].type == "string"
        assert properties["int_param"].type == "integer"
        assert properties["float_param"].type == "number"
        assert properties["bool_param"].type == "boolean"
        assert properties["list_param"].type == "array"
        assert properties["dict_param"].type == "object"
        assert properties["untyped_param"].type == "string"
