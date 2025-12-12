from moysklad_api.methods import MSMethod
from moysklad_api.types import Assortment, MetaArray


class GetAssortment(MSMethod):
    __return__ = MetaArray[Assortment]
    __api_method__ = "entity/assortment"
