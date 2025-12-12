from moysklad_api.methods import MSMethod
from moysklad_api.types import CurrentStock


class GetCurrentStock(MSMethod):
    __return__ = list[CurrentStock]
    __api_method__ = "report/stock/all/current"
