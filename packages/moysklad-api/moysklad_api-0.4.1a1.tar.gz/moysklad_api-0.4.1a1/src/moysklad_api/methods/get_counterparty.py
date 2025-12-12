from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Counterparty


class GetCounterparty(MSMethod):
    __return__ = Counterparty
    __api_method__ = "entity/counterparty"

    id: str = Field(..., alias="counterparty_id")
