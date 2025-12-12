from pydantic import BaseModel


class Barcode(BaseModel):
    ean13: str | None = None
    ean8: str | None = None
    code128: str | None = None
    gtin: str | None = None
    upc: str | None = None
