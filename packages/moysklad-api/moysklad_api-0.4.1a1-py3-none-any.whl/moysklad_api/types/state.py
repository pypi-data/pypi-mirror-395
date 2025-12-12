from pydantic import Field

from ..enums import EntityType
from .entity import Entity


class State(Entity):
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    name: str | None = Field(None, alias="name")
    color: int | None = Field(None, alias="color")
    state_type: str | None = Field(None, alias="stateType")
    entity_type: EntityType | None = Field(None, alias="entityType")
