from ..models import Message


class MSGService:
    def __init__(self) -> None:
        self.messages: dict[str : list[Message]] = {}
        self.unread_channels: dict[str:bool] = {}

    def add_message(self, channel_id: str, author: str, content: str) -> None:
        msgs: list[Message] = self.messages.get(channel_id)
        if self.messages.get(channel_id) is None:
            self.messages[channel_id] = [Message(author, content)]
        else:
            msgs.append(Message(author, content))

        self.unread_channels[channel_id] = True
        self.notify_admin_unread()

    def get_channel_messages(self, chan_id: str) -> list[Message] | None:
        if (msgs := self.messages.get(chan_id)) is not None:
            del self.unread_channels[chan_id]
            return msgs

        return None

    def notify_admin_unread(self) -> list[str] | None:
        unread_channels_keys: list[str] = list(self.unread_channels.keys())
        notify_condition: bool = len(unread_channels_keys) >= 7
        if notify_condition:
            # print(
            #     f"Admin: unread messages in {len(unread_channels_keys)} conversations."
            # )
            return unread_channels_keys
        return None
