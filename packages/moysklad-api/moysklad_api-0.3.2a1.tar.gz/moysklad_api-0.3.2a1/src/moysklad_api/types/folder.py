from pydantic import BaseModel, Field

from .meta import Meta


class Folder(BaseModel):
    meta: Meta
    name: str = Field(..., alias="name")
    path_name: str = Field(..., alias="pathName")
