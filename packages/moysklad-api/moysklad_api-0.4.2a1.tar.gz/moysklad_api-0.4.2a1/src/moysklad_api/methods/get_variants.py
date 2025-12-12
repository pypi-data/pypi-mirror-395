from moysklad_api.methods import MSMethod
from moysklad_api.types import MetaArray, Variant


class GetVariants(MSMethod):
    __return__ = MetaArray[Variant]
    __api_method__ = "entity/variant"
