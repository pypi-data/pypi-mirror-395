# standard
# third party
import pydantic

# custom


class Model(pydantic.BaseModel):
    name: str
    display_name: str
    origin: str
    version: str | None = None
