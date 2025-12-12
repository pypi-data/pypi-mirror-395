from pydantic import Field

from .currency import Currency
from .entity import Entity
from .meta import Meta
from .price_type import PriceType


class SalePrice(Entity):
    meta: Meta | None = None
    value: float
    currency: Currency | None = Field(None, alias="currency")
    price_type: PriceType | None = Field(None, alias="priceType")
