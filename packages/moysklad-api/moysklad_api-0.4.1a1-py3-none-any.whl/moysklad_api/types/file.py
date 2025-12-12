from pydantic import BaseModel


class File(BaseModel):
    filename: str | None = None
    content: str | None = None
