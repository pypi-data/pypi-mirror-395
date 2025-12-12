from typing import Any

from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Barcode, BuyPrice, MinPrice, Pack, SalePrice, Variant


class UpdateVariant(MSMethod[Variant]):
    __return__ = Variant
    __api_method__ = "entity/variant"

    id: str = Field(..., alias="variant_id")
    archived: bool | None = Field(None, alias="archived")
    barcodes: list[Barcode] | None = Field(None, alias="barcodes")
    buy_price: BuyPrice | None = Field(None, alias="buyPrice")
    characteristics: list[dict[str, Any]] | None = Field(None, alias="characteristics")
    code: str | None = Field(None, alias="code")
    description: str | None = Field(None, alias="description")
    discount_prohibited: bool | None = Field(None, alias="discountProhibited")
    external_code: str | None = Field(None, alias="externalCode")
    images: dict | None = Field(None, alias="images")
    min_price: MinPrice | None = Field(None, alias="minPrice")
    minimum_stock: dict[str, Any] | None = Field(None, alias="minimumStock")
    name: str | None = Field(None, alias="name")
    packs: list[Pack] | None = Field(None, alias="packs")
    sale_prices: list[SalePrice] | None = Field(None, alias="salePrices")
    product: dict[str, Any] | None = Field(None, alias="product")
