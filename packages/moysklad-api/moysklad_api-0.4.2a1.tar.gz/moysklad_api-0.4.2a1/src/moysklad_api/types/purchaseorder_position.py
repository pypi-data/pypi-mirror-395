from pydantic import Field

from .assortment import Assortment
from .entity import Entity
from .pack import Pack


class PurchaseOrderPosition(Entity):
    account_id: str | None = Field(None, alias="accountId")
    assortment: Assortment | None = Field(None, alias="assortment")
    discount: float | None = Field(None, alias="discount")
    id: str | None = Field(None, alias="id")
    pack: Pack | None = Field(None, alias="pack")
    price: float | None = Field(None, alias="price")
    quantity: float | None = Field(None, alias="quantity")
    shipped: float | None = Field(None, alias="shipped")
    in_transit: float | None = Field(None, alias="inTransit")
    vat: int | None = Field(None, alias="vat")
    vat_enabled: bool | None = Field(None, alias="vatEnabled")
