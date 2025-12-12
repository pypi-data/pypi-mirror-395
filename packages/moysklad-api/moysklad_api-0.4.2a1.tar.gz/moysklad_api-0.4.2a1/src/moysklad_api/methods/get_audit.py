from pydantic import Field

from moysklad_api.methods import MSMethod
from moysklad_api.types import Audit


class GetAudit(MSMethod):
    __return__ = Audit
    __api_method__ = "audit"

    id: str = Field(..., alias="audit_id")
