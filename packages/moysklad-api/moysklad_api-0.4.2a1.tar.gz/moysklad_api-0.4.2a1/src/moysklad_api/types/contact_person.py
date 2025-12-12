from datetime import datetime

from pydantic import Field

from .entity import Entity
from .meta import Meta


class ContactPerson(Entity):
    account_id: str | None = Field(None, alias="accountId")
    agent: Meta | None = Field(None, alias="agent")
    description: str | None = Field(None, alias="description")
    email: str | None = Field(None, alias="email")
    external_code: str | None = Field(None, alias="externalCode")
    id: str | None = Field(None, alias="id")
    name: str | None = Field(None, alias="name")
    phone: str | None = Field(None, alias="phone")
    position: str | None = Field(None, alias="position")
    updated: datetime | None = Field(None, alias="updated")
