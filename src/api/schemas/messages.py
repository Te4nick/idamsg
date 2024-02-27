from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str = Field(
        ...,
        description="Message content",
        min_length=1,
        max_length=255,
    )
    author: str = Field(
        ...,
        description="Message author nickname",
        min_length=3,
        max_length=50,
    )


class MessageIn(Message):
    channel: str = Field(
        ...,
        description="Channel string id to post message to",
        min_length=1,
        max_length=50,
    )


class MessageAllOut(BaseModel):
    messages: list[Message] = Field(
        [],
        description="List of messages from channel",
        examples=[
            [Message(content="string", author="string")],
        ],
    )
