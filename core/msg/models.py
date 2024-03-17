from django.db import models


class Message:
    author: str
    content: str

    def __init__(self, author: str, content: str) -> None:
        self.author: str = author
        self.content: str = content


class Image:
    done: bool
    result: str

    def __init__(self, done: bool = False, result: str | None = None) -> None:
        self.done: bool = done
        self.result: str = result
