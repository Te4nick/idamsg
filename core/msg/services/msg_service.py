from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
from ..models import Message, Image


class MSGService:
    def __init__(self, image_output_path: str = "./static/png") -> None:
        self.messages: dict[str : list[Message]] = {}
        self.unread_channels: dict[str:bool] = {}
        self.image_output_path = image_output_path + (
            "/" if image_output_path[-1] != "/" else ""
        )

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
            print(
                f"Admin: unread messages in {len(unread_channels_keys)} conversations."
            )
            return unread_channels_keys
        return None

    def generate_most_common_words(self) -> str | None:
        all_words = " ".join(
            [
                message.content
                for chan in self.messages.values()
                for message in chan.messages
            ]
        ).split()
        word_freq = Counter(all_words)

        common_words = word_freq.most_common(5)  # Display top 5 most common words

        if len(common_words) < 5:
            return None

        words, freq = zip(*common_words)

        plt.bar(words, freq)
        plt.xlabel("Words")
        plt.ylabel("Count")
        plt.title("Top 5 Most Common Words")

        time_formatted: str = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        filename: str = f"MostCommonWords_{time_formatted}.png"
        plt.savefig(self.image_output_path + filename, bbox_inches="tight")

        return self.image_output_path + filename
