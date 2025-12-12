from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Webhook


class GetWebhook(MSMethod):
    __return__ = Webhook
    __api_method__ = "entity/webhook"

    id: str = Field(..., alias="webhook_id")
