from pydantic import Field

from moysklad_api.methods import GetAudit
from moysklad_api.types import Event, MetaArray


class GetEvents(GetAudit):
    __return__ = MetaArray[Event]
    __api_method__ = "audit/{id}/events"

    id: str = Field(..., alias="audit_id")
