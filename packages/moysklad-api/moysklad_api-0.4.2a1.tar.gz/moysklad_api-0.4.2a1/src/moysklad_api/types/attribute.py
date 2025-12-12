from pydantic import Field

from .entity import Entity


class Attribute(Entity):
    id: str | None = Field(None, alias="id")
    name: str | None = Field(None, alias="name")
    type: str | None = Field(None, alias="type")
    value: str | None = Field(None, alias="value")
