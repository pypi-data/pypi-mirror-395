from datetime import datetime

from pydantic import Field

from ..enums import EntityType, EventType, ObjectType, Source
from .entity import Entity
from .event import Event


class Audit(Entity):
    entity_type: EntityType | None = Field(None, alias="entityType")
    event_type: EventType | None = Field(None, alias="eventType")
    events: Event | list[Event] | None = Field(None, alias="events")
    id: str | None = Field(None, alias="id")
    info: str | None = Field(None, alias="info")
    moment: datetime | None = Field(None, alias="moment")
    object_count: int | None = Field(None, alias="objectCount")
    object_type: ObjectType | None = Field(None, alias="objectType")
    source: Source | None = Field(None, alias="source")
    support_access: bool | None = Field(None, alias="supportAccess")
    uid: str | None = Field(None, alias="uid")
