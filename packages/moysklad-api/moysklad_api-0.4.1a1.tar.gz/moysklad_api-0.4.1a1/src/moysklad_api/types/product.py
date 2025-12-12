from datetime import datetime

from pydantic import Field

from .alcoholic import Alcoholic
from .barcode import Barcode
from .buy_price import BuyPrice
from .country import Country
from .entity import Entity
from .file import File
from .group import Group
from .image import Image
from .min_price import MinPrice
from .owner import Owner
from .pack import Pack
from .product_folder import ProductFolder
from .sale_price import SalePrice
from .supplier import Supplier
from .uom import Uom


class Product(Entity):
    id: str | None = Field(None, alias="id")
    account_id: str | None = Field(None, alias="accountId")
    archived: bool | None = Field(None, alias="archived")
    discount_prohibited: bool | None = Field(None, alias="discountProhibited")
    external_code: str | None = Field(None, alias="externalCode")
    group: Group | None = Field(None, alias="group")
    name: str | None = Field(None, alias="name")
    path_name: str | None = Field(None, alias="pathName")
    shared: bool | None = Field(None, alias="shared")
    updated: datetime | None = Field(None, alias="updated")
    use_parent_vat: bool | None = Field(None, alias="useParentVat")
    variants_count: int | None = Field(None, alias="variantsCount")
    alcoholic: Alcoholic | None = Field(None, alias="alcoholic")
    article: str | None = Field(None, alias="article")
    attributes: list[dict] | None = Field(None, alias="attributes")
    barcodes: list[Barcode] | None = Field(None, alias="barcodes")
    buy_price: BuyPrice | None = Field(None, alias="buyPrice")
    code: str | None = Field(None, alias="code")
    country: Country | None = Field(None, alias="country")
    description: str | None = Field(None, alias="description")
    effective_vat: int | None = Field(None, alias="effectiveVat")
    effective_vat_enabled: bool | None = Field(None, alias="effectiveVatEnabled")
    files: dict | list[File] | None = Field(None, alias="files")
    images: dict | list[Image] | None = Field(None, alias="images")
    is_serial_trackable: bool | None = Field(None, alias="isSerialTrackable")
    min_price: MinPrice | None = Field(None, alias="minPrice")
    minimum_balance: float | None = Field(None, alias="minimumBalance", deprecated=True)
    minimum_stock: dict | None = Field(None, alias="minimumStock")
    owner: Owner | None = Field(None, alias="owner")
    packs: list[Pack] | None = Field(None, alias="packs")
    partial_disposal: bool | None = Field(None, alias="partialDisposal")
    payment_item_type: str | None = Field(None, alias="paymentItemType")
    ppe_type: str | None = Field(None, alias="ppeType")
    product_folder: ProductFolder | None = Field(None, alias="productFolder")
    sale_prices: list[SalePrice] | None = Field(None, alias="salePrices")
    supplier: Supplier | None = Field(None, alias="supplier")
    sync_id: str | None = Field(None, alias="syncId")
    tax_system: str | None = Field(None, alias="taxSystem")
    things: list[str] | None = Field(None, alias="things")
    tnved: str | None = Field(None, alias="tnved")
    tracking_type: str | None = Field(None, alias="trackingType")
    uom: Uom | None = Field(None, alias="uom")
    vat: int | None = Field(None, alias="vat")
    vat_enabled: bool | None = Field(None, alias="vatEnabled")
    volume: float | None = Field(None, alias="volume")
    weight: float | None = Field(None, alias="weight")
