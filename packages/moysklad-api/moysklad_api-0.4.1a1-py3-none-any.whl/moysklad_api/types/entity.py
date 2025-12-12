from pydantic import BaseModel, ConfigDict

from .meta import Meta


class Entity(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    meta: Meta | None = None

    @property
    def is_expanded(self) -> bool:
        for name, value in self.model_dump().items():
            if name != "meta" and value is not None:
                return True
        return False
