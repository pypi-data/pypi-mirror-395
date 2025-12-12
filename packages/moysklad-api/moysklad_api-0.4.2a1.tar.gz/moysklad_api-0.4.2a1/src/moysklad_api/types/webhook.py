from pydantic import Field

from ..enums import EntityType
from .audit import Audit
from .entity import Entity
from .event import Event
from .meta import Meta


class Webhook(Entity):
    meta: Meta | None = None
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    entity_type: EntityType | None = Field(None, alias="entityType")
    url: str | None = Field(None, alias="url")
    method: str | None = Field(None, alias="method")
    enabled: bool | None = Field(None, alias="enabled")
    action: str | None = Field(None, alias="action")
    events: list[Event] | None = Field(None, alias="events")
    audit_context: Audit | None = Field(None, alias="auditContext")
