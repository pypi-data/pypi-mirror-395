from pydantic import Field

from moysklad_api.methods.base import MSMethod
from moysklad_api.types import Product


class UpdateProduct(MSMethod[Product]):
    __return__ = Product
    __api_method__ = "entity/product"

    id: str = Field(..., alias="product_id")
    name: str | None = None
    description: str | None = None
    code: str | None = None
    external_code: str | None = None
    archived: bool | None = None
    article: str | None = None
    group: str | None = None
    product_folder: str | None = Field(None, alias="productFolder")
    sale_prices: list[dict] | None = Field(None, alias="salePrices")
    attributes: list[dict] | None = None
    barcodes: list[dict] | None = None
    min_price: dict | None = Field(None, alias="minPrice")
    uom: str | None = None
    tracking_type: str | None = Field(None, alias="trackingType")
    is_serial_trackable: bool | None = Field(None, alias="isSerialTrackable")
    files: list[dict] | None = None
    images: list[dict] | None = None
    packs: list[dict] | None = None
    owner: str | None = None
    supplier: str | None = None
    shared: bool | None = None
    effective_vat: int | None = Field(None, alias="effectiveVat")
    discount_prohibited: bool | None = Field(None, alias="discountProhibited")
    use_parent_vat: bool | None = Field(None, alias="useParentVat")
