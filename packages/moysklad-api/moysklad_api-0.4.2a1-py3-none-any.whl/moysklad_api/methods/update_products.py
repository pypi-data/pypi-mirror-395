from moysklad_api.methods.base import MSMethod
from moysklad_api.types import Product


class UpdateProducts(MSMethod[Product]):
    __return__ = list[Product]
    __api_method__ = "entity/product"

    data: list[Product]
