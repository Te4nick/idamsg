from dataclasses import dataclass


@dataclass
class Message:
    author: str
    msg: str
