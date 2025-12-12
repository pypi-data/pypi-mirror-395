from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import PurchaseOrder


class GetPurchaseOrder(MSMethod):
    __return__ = PurchaseOrder
    __api_method__ = "entity/purchaseorder"

    id: str = Field(..., alias="purchaseorder_id")
