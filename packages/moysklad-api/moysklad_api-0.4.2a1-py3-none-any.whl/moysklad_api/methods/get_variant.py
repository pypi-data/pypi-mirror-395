from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Variant


class GetVariant(MSMethod):
    __return__ = Variant
    __api_method__ = "entity/variant"

    id: str = Field(..., alias="variant_id")
