from pydantic import Field

from .entity import Entity


class Supplier(Entity):
    id: str | None = None
    name: str | None = None
    phone: str | None = None
    company_type: str | None = Field(None, alias="companyType")
