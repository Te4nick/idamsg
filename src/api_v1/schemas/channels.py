from annotated_types import Ge
from pydantic import BaseModel, Field
from typing import Annotated


class Channel(BaseModel):
    id: str = Field(
        ...,
        description="Channel unique identifier",
        min_length=3,
        max_length=50,
    )


class ChannelAllUnreadOut(BaseModel):
    count: Annotated[int, Ge(0)]
    channels: list[Channel]
