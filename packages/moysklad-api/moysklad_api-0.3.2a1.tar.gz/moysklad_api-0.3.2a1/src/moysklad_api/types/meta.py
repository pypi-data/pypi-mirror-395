from pydantic import BaseModel, ConfigDict, Field


class Meta(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )

    href: str
    type: str | None = Field(None, alias="type")
    metadata_href: str | None = Field(None, alias="metadataHref")
    media_type: str | None = Field("application/json", alias="mediaType")
    uuid_href: str | None = Field(None, alias="uuidHref")
    download_href: str | None = Field(None, alias="downloadHref")
    size: int | None = Field(None, alias="size")
    limit: int | None = Field(None, alias="limit")
    offset: int | None = Field(None, alias="offset")
    next_href: str | None = Field(None, alias="nextHref")
    previous_href: str | None = Field(None, alias="previousHref")
