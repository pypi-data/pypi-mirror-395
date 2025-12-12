from datetime import datetime

from pydantic import Field

from .account import Account
from .actual_address_full import ActualAddressFull
from .bouns_program import BonusProgram
from .contact_person import ContactPerson
from .entity import Entity
from .file import File
from .group import Group
from .note import Note
from .owner import Owner
from .price_type import PriceType
from .state import State


class Counterparty(Entity):
    account_id: str | None = Field(None, alias="accountId")
    accounts: Account | None = Field(None, alias="accounts")
    actual_address: str | None = Field(None, alias="actualAddress")
    actual_address_full: ActualAddressFull | None = Field(
        None, alias="actualAddressFull"
    )
    archived: bool | None = Field(None, alias="archived")
    attributes: list[dict] | None = Field(None, alias="attributes")
    bonus_points: int | None = Field(None, alias="bonusPoints")
    bonus_program: BonusProgram | None = Field(None, alias="bonusProgram")
    code: str | None = Field(None, alias="code")
    company_type: str | None = Field(None, alias="companyType")
    contactpersons: ContactPerson | list[ContactPerson] | None = Field(
        None, alias="contactPersons"
    )
    created: datetime | None = Field(None, alias="created")
    description: str | None = Field(None, alias="description")
    discount_card_number: str | None = Field(None, alias="discountCardNumber")
    discounts: list[dict] | None = Field(None, alias="discounts")
    email: str | None = Field(None, alias="email")
    external_code: str | None = Field(None, alias="externalCode")
    fax: str | None = Field(None, alias="fax")
    files: File | None = Field(None, alias="files")
    group: Group | None = Field(None, alias="group")
    id: str | None = Field(None, alias="id")
    name: str | None = Field(None, alias="name")
    notes: Note | list[Note] | None = Field(None, alias="notes")
    owner: Owner | None = Field(None, alias="owner")
    phone: str | None = Field(None, alias="phone")
    price_type: PriceType | None = Field(None, alias="priceType")
    sales_amount: int | None = Field(None, alias="salesAmount")
    shared: bool | None = Field(None, alias="shared")
    state: State | None = Field(None, alias="state")
    sync_id: str | None = Field(None, alias="syncId")
    tags: list[str] | None = Field(None, alias="tags")
    updated: datetime | None = Field(None, alias="updated")
