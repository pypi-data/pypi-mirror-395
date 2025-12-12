from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Demand


class GetDemand(MSMethod):
    __return__ = Demand
    __api_method__ = "entity/demand"

    id: str = Field(..., alias="demand_id")
