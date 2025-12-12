from moysklad_api.methods.base import MSMethod
from moysklad_api.types import Variant


class UpdateVariants(MSMethod[Variant]):
    __return__ = list[Variant]
    __api_method__ = "entity/variant"

    data: list[Variant]
