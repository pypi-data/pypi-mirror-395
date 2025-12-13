from typing import Any
from pydantic import BaseModel, HttpUrl, Field


class ExtractedLink(BaseModel):
    url: HttpUrl
    title: str | None = None
    description: str | None = None
    icon_url: HttpUrl | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractionResult(BaseModel):
    source_url: HttpUrl
    service_type: str | None = None
    links: list[ExtractedLink]
    raw_html: str | None = None
    extraction_timestamp: str | None = None
    errors: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
