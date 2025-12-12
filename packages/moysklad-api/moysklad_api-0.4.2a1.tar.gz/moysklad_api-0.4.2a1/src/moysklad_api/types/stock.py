from pydantic import BaseModel, Field

from .folder import Folder
from .image import Image
from .meta import Meta
from .uom import Uom


class CurrentStock(BaseModel):
    assortment_id: str = Field(..., alias="assortmentId")
    stock: float = Field(..., alias="stock")


class Stock(BaseModel):
    article: str | None = Field(None, alias="article")
    code: str | None = Field(..., alias="code")
    external_code: str | None = Field(..., alias="externalCode")
    folder: Folder | None = Field(None, alias="folder")
    image: Image | None = Field(None, alias="image")
    in_transit: float | None = Field(..., alias="inTransit")
    meta: Meta = Field(..., alias="meta")
    name: str = Field(..., alias="name")
    price: float = Field(..., alias="price")
    quantity: float = Field(..., alias="quantity")
    reserve: float = Field(..., alias="reserve")
    sale_price: float = Field(..., alias="salePrice")
    stock: float = Field(..., alias="stock")
    stock_days: float = Field(..., alias="stockDays")
    uom: Uom | None = Field(None, alias="uom")
