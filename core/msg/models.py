from django.db import models
from uuid import UUID


class Message:
    author: str
    content: str

    def __init__(self, author: str, content: str) -> None:
        self.author: str = author
        self.content: str = content

    def __eq__(self, other: "Message") -> bool:
        return self.author == other.author and self.content == other.content


class Image:
    done: bool
    result: str

    def __init__(self, done: bool = False, result: str | None = None) -> None:
        self.done: bool = done
        self.result: str = result


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.id == other.id
            and self.done == other.done
            and self.result == other.result
        )
