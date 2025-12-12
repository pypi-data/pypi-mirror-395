from datetime import datetime

from pydantic import Field

from ..enums import EntityType, EventType, ObjectType, Source
from .entity import Entity
from .event import Event


class Audit(Entity):
    entity_type: EntityType = Field(None, alias="entityType")
    event_type: EventType = Field(None, alias="eventType")
    events: Event | list[Event] = Field(None, alias="events")
    id: str = Field(None, alias="id")
    info: str = Field(None, alias="info")
    moment: datetime = Field(None, alias="moment")
    object_count: int = Field(None, alias="objectCount")
    object_type: ObjectType = Field(None, alias="objectType")
    source: Source = Field(None, alias="source")
    support_access: bool = Field(None, alias="supportAccess")
    uid: str = Field(None, alias="uid")
