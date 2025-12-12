from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Product


class GetProduct(MSMethod):
    __return__ = Product
    __api_method__ = "entity/product"

    id: str = Field(..., alias="product_id")
