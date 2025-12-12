from pydantic import BaseModel, Field

from .country import Country
from .region import Region


class ActualAddressFull(BaseModel):
    add_info: str | None = Field(None, alias="addInfo")
    apartment: str | None = Field(None, alias="apartment")
    city: str | None = Field(None, alias="city")
    comment: str | None = Field(None, alias="comment")
    fias_code_ru: str | None = Field(None, alias="fiasCode__ru")
    country: Country | None = Field(None, alias="country")
    house: str | None = Field(None, alias="house")
    postal_code: str | None = Field(None, alias="postalCode")
    region: Region | None = Field(None, alias="region")
    street: str | None = Field(None, alias="street")
