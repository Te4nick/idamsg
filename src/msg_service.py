from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime


class MSGService:
    def __init__(self, image_output_path: str = "./static/png") -> None:
        self.messages: dict[str : list[tuple[str:str]]] = {}
        self.unread: dict[str:bool] = {}
        self.image_output_path = image_output_path + (
            "/" if image_output_path[-1] != "/" else ""
        )

    def add_message(self, ch_id: str, author: str, msg: str) -> None:
        if ch_id in self.messages:
            self.messages[ch_id].append((author, msg))
        else:
            self.messages[ch_id] = [(author, msg)]
        self.unread[ch_id] = True
        self.notify_admin_unread()

    def get_channel_messages(self, ch_id: str) -> list[tuple[str, str]] | None:
        if ch_id in self.messages:
            self.unread[ch_id] = False
            return self.messages[ch_id]
        return None

    def notify_admin_unread(self) -> bool:
        unread_count = sum(self.unread.values())
        if unread_count >= 7:
            print(f"Admin: unread messages in {unread_count} conversations.")
            return True
        return False

    def generate_most_common_words(self) -> str | None:
        all_words = " ".join(
            [message[1] for messages in self.messages.values() for message in messages]
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

        return filename
