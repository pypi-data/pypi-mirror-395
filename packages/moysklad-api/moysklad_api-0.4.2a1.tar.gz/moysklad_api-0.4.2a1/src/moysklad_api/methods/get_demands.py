from moysklad_api.methods import MSMethod
from moysklad_api.types import Demand, MetaArray


class GetDemands(MSMethod):
    __return__ = MetaArray[Demand]
    __api_method__ = "entity/demand"
