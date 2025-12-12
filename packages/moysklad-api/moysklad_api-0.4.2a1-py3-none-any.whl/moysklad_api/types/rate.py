from pydantic import BaseModel

from .currency import Currency


class Rate(BaseModel):
    currency: Currency
    value: float | None = None
