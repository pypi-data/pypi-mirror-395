from moysklad_api.methods import MSMethod
from moysklad_api.types import MetaArray, Webhook


class GetWebhooks(MSMethod):
    __return__ = MetaArray[Webhook]
    __api_method__ = "entity/webhook"
