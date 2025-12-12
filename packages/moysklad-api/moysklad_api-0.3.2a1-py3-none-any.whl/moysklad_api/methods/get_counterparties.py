from moysklad_api.methods import MSMethod
from moysklad_api.types import Counterparty, MetaArray


class GetCounterparties(MSMethod):
    __return__ = MetaArray[Counterparty]
    __api_method__ = "entity/counterparty"
