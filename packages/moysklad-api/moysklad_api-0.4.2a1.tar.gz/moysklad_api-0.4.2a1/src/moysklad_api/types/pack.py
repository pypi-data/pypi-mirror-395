from uuid import UUID

from .entity import Entity
from .meta import Meta


class Pack(Entity):
    barcodes: list[dict] | None = None
    id: UUID
    quantity: float
    uom: Meta
