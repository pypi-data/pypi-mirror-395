from moysklad_api.methods import MSMethod
from moysklad_api.types import MetaArray, Stock


class GetStock(MSMethod):
    __return__ = MetaArray[Stock]
    __api_method__ = "report/stock/all"
