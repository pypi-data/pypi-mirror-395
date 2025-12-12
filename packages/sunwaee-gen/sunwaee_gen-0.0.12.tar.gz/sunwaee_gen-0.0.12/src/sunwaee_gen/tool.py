# standard
import inspect
import typing

# third party
import pydantic

# custom


class Param(pydantic.BaseModel):
    type: str
    description: str


class Parameters(pydantic.BaseModel):
    type: str = "object"
    properties: dict[str, Param]
    required: list[str]

    @pydantic.field_validator("properties")
    @classmethod
    def check_properties_not_empty(cls, v):
        if not isinstance(v, dict) or not v:
            raise ValueError("properties must be a non-empty dict")
        return v

    @pydantic.field_validator("required", mode="before")
    @classmethod
    def check_required_in_properties(cls, v, info):
        properties = info.data.get("properties", {})
        for req in v:
            if req not in properties:
                raise ValueError(f"required field '{req}' not in properties")
        return v


class Function(pydantic.BaseModel):
    name: str
    description: str
    parameters: Parameters


class Tool(pydantic.BaseModel):
    type: typing.Literal["function"] = "function"
    function: Function

    @classmethod
    def from_dict(cls, data: dict) -> "Tool":
        func = data.get("function", {})
        params = func.get("parameters", {})
        return cls(
            function=Function(
                name=func["name"],
                description=func["description"],
                parameters=params,
            )
        )

    @classmethod
    def from_list(cls, items: list[dict]) -> "list[Tool]":
        return [cls.from_dict(item) for item in items]


def T(ignore: list[str] = []):
    def decorator(func: typing.Callable) -> Tool:
        sig = inspect.signature(func)
        properties = {}
        required = []
        ignore_params = ignore or []

        # tool desc
        tool_description = ""
        param_descriptions = {}

        if func.__doc__:
            doc_lines = func.__doc__.strip().split("\n")
            description_lines = []

            for line in doc_lines:
                line = line.strip()
                if not line:
                    continue

                # param desc
                if ":" in line and not line.startswith("#"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        param_name = parts[0].strip()
                        param_desc = parts[1].strip()
                        if " " not in param_name:
                            param_descriptions[param_name] = param_desc
                            continue

                description_lines.append(line)

            tool_description = " ".join(description_lines).strip()

        if not tool_description:
            tool_description = f"Function {func.__name__}"

        for param_name, param in sig.parameters.items():
            if param_name == "self" or param_name in ignore_params:
                continue

            # param type
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation in (list, dict):
                    param_type = "array" if param.annotation == list else "object"

            properties[param_name] = Param(
                type=param_type,
                description=param_descriptions.get(
                    param_name, f"Parameter {param_name}"
                ),
            )

            # required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        tool = Tool(
            function=Function(
                name=func.__name__,
                description=tool_description,
                parameters=Parameters(properties=properties, required=required),
            )
        )

        tool._execute = func

        return tool

    return decorator
