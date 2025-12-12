from pydantic import BaseModel

from ..enums import OverheadDistribution


class Overhead(BaseModel):
    sum: float
    distribution: OverheadDistribution
