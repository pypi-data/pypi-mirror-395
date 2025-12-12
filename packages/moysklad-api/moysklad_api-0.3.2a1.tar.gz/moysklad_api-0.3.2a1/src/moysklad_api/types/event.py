from datetime import datetime
from typing import Any

from pydantic import Field

from ..enums import EntityType, EventType, ObjectType, Source
from .diff import Diff
from .entity import Entity
from .meta import Meta


class Event(Entity):
    meta: Meta | None = None
    event_type: EventType = Field(None, alias="eventType")
    entity_type: EntityType = Field(None, alias="entityType")
    diff: dict[str, Diff | list[Diff] | Any] | None = Field(None, alias="diff")
    name: str = Field(None, alias="name")
    entity: Entity = Field(None, alias="entity")
    moment: datetime = Field(None, alias="moment")
    object_count: int = Field(None, alias="objectCount")
    object_type: ObjectType = Field(None, alias="objectType")
    source: Source = Field(None, alias="source")
    support_access: bool = Field(None, alias="supportAccess")
    uid: str = Field(None, alias="uid")
