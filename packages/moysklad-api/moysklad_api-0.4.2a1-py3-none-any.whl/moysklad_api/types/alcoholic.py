from pydantic import BaseModel


class Alcoholic(BaseModel):
    excise: bool
    type: int
    strength: int
    volume: float
