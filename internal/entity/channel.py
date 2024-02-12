class Channel:
    def __init__(self):
        self.messages: list[tuple[str: str]] = []

    def get_messages(self) -> list[str]:
        self.unread = False
        return self.messages

    def add_message(self, msg: str) -> None:
        self.messages.append(msg)
        self.unread = True
