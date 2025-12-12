from pydantic import BaseModel

from .currency import Currency


class MinPrice(BaseModel):
    value: float
    currency: Currency
