from pydantic import Field

from .attribute import Attribute
from .barcode import Barcode
from .buy_price import BuyPrice
from .entity import Entity
from .group import Group
from .image import Image
from .min_price import MinPrice
from .owner import Owner
from .product import Product
from .sale_price import SalePrice
from .supplier import Supplier
from .uom import Uom


class Assortment(Entity):
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    owner: Owner | None = Field(None, alias="owner")
    shared: bool | None = Field(None, alias="shared")
    group: Group | None = Field(None, alias="group")
    updated: str | None = Field(None, alias="updated")
    name: str | None = Field(None, alias="name")
    description: str | None = Field(None, alias="description")
    code: str | None = Field(None, alias="code")
    external_code: str | None = Field(None, alias="externalCode")
    archived: bool | None = Field(None, alias="archived")
    path_name: str | None = Field(None, alias="pathName")
    use_parent_vat: bool | None = Field(None, alias="useParentVat")
    vat: int | None = Field(None, alias="vat")
    vat_enabled: bool | None = Field(None, alias="vatEnabled")
    effective_vat: int | None = Field(None, alias="effectiveVat")
    effective_vat_enabled: bool | None = Field(None, alias="effectiveVatEnabled")
    uom: Uom | None = Field(None, alias="uom")
    images: dict | list[Image] | None = Field(None, alias="images")
    min_price: MinPrice | None = Field(None, alias="minPrice")
    sale_prices: list[SalePrice] | None = Field(None, alias="salePrices")
    attributes: list[Attribute] | None = Field(None, alias="attributes")
    supplier: Supplier | None = Field(None, alias="supplier")
    buy_price: BuyPrice | None = Field(None, alias="buyPrice")
    article: str | None = Field(None, alias="article")
    weight: float | None = Field(None, alias="weight")
    volume: float | None = Field(None, alias="volume")
    barcodes: list[Barcode] | None = Field(None, alias="barcodes")
    variants_count: int | None = Field(None, alias="variantsCount")
    product: Product | None = Field(None, alias="product")
    is_serial_trackable: bool | None = Field(None, alias="isSerialTrackable")
    stock: float | None = Field(None, alias="stock")
    reserve: float | None = Field(None, alias="reserve")
    in_transit: float | None = Field(None, alias="inTransit")
    quantity: float | None = Field(None, alias="quantity")
