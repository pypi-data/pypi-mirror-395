from datetime import datetime

from .entity import BaseModel
from .meta import Meta


class Image(BaseModel):
    filename: str | None = None
    meta: Meta | None = None
    miniature: Meta | None = None
    size: int | None = None
    tiny: Meta | None = None
    title: str | None = None
    updated: datetime | None = None
