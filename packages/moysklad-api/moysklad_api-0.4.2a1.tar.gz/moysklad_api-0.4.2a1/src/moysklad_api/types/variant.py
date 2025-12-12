from datetime import datetime
from typing import Any

from pydantic import Field

from . import Product
from .barcode import Barcode
from .buy_price import BuyPrice
from .entity import Entity
from .image import Image
from .min_price import MinPrice
from .pack import Pack
from .sale_price import SalePrice


class Variant(Entity):
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    archived: bool | None = Field(None, alias="archived")
    barcodes: list[Barcode] | None = Field(None, alias="barcodes")
    buy_price: BuyPrice | None = Field(None, alias="buyPrice")
    characteristics: list[dict[str, Any]] | None = Field(None, alias="characteristics")
    code: str | None = Field(None, alias="code")
    description: str | None = Field(None, alias="description")
    discount_prohibited: bool | None = Field(None, alias="discountProhibited")
    external_code: str | None = Field(None, alias="externalCode")
    images: Image | list[Image] | None = Field(None, alias="images")
    min_price: MinPrice | None = Field(None, alias="minPrice")
    minimum_stock: dict[str, Any] | None = Field(None, alias="minimumStock")
    name: str | None = Field(None, alias="name")
    packs: list[Pack] | None = Field(None, alias="packs")
    product: Product | None = Field(None, alias="product")
    sale_prices: list[SalePrice] | None = Field(None, alias="salePrices")
    things: list[str] | None = Field(None, alias="things")
    updated: datetime | None = Field(None, alias="updated")
