from moysklad_api.methods import MSMethod
from moysklad_api.types import MetaArray, PurchaseOrder


class GetPurchaseOrders(MSMethod):
    __return__ = MetaArray[PurchaseOrder]
    __api_method__ = "entity/purchaseorder"
