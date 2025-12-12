from pydantic import Field

from .entity import Entity


class PriceType(Entity):
    id: str | None = Field(None, alias="id")
    name: str | None = Field(None, alias="name")
    external_code: str | None = Field(None, alias="externalCode")
