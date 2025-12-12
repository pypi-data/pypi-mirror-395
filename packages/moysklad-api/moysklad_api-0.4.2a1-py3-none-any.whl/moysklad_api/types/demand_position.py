from pydantic import Field

from .assortment import Assortment
from .entity import Entity


class DemandPosition(Entity):
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    quantity: int | None = Field(None, alias="quantity")
    price: float | None = Field(None, alias="price")
    discount: float | None = Field(None, alias="discount")
    vat: int | None = Field(None, alias="vat")
    vat_enabled: bool | None = Field(None, alias="vatEnabled")
    assortment: Assortment | None = Field(None, alias="assortment")
