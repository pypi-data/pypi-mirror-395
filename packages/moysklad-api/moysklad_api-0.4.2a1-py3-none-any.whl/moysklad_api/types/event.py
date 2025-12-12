from datetime import datetime
from typing import Any

from pydantic import Field

from ..enums import EntityType, EventType, ObjectType, Source
from .diff import Diff
from .entity import Entity
from .meta import Meta


class Event(Entity):
    meta: Meta | None = None
    event_type: EventType | None = Field(None, alias="eventType")
    entity_type: EntityType | None = Field(None, alias="entityType")
    diff: dict[str, Diff | list[Diff] | Any] | None = Field(None, alias="diff")
    name: str | None = Field(None, alias="name")
    entity: Entity | None = Field(None, alias="entity")
    moment: datetime | None = Field(None, alias="moment")
    object_count: int | None = Field(None, alias="objectCount")
    object_type: ObjectType | None = Field(None, alias="objectType")
    source: Source | None = Field(None, alias="source")
    support_access: bool | None = Field(None, alias="supportAccess")
    uid: str | None = Field(None, alias="uid")
