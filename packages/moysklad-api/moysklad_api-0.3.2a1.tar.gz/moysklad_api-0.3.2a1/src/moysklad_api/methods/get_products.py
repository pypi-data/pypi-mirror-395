from moysklad_api.methods import MSMethod
from moysklad_api.types import MetaArray, Product


class GetProducts(MSMethod):
    __return__ = MetaArray[Product]
    __api_method__ = "entity/product"
