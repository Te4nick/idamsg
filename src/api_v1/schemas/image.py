from pydantic import BaseModel, Field


class Image(BaseModel):
    path: str = Field(
        ...,
        description="Path to static image resource",
    )
