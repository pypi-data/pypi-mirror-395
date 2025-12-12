from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from .meta import Meta


T = TypeVar("T", bound=BaseModel)


class MetaArray(BaseModel, Generic[T]):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    rows: list[T]
    meta: Meta
