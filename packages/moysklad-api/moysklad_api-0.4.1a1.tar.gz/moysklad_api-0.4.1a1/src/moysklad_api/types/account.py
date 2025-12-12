from datetime import datetime

from pydantic import Field

from .entity import Entity
from .meta import Meta


class Account(Entity):
    account_id: str | None | None = Field(None, alias="accountId")
    account_number: str | None | None = Field(None, alias="accountNumber")
    bank_location: str | None | None = Field(None, alias="bankLocation")
    bank_name: str | None | None = Field(None, alias="bankName")
    bic: str | None | None = Field(None, alias="bic")
    correspondent_account: str | None | None = Field(None, alias="correspondentAccount")
    id: str | None | None = Field(None, alias="id")
    is_default: bool | None | None = Field(None, alias="isDefault")
    meta: Meta = Field(..., alias="meta")
    updated: datetime | None = Field(None, alias="updated")
