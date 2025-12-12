from pydantic import BaseModel, ConfigDict, Field

from .entity import Entity


class Diff(BaseModel):
    model_config = ConfigDict(extra="allow")
    old_value: str | Entity = Field(..., alias="oldValue")
    new_value: str | Entity = Field(..., alias="newValue")
