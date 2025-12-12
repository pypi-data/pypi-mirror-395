from pydantic import BaseModel

from .currency import Currency


class BuyPrice(BaseModel):
    value: float
    currency: Currency
