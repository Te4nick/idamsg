from collections import Counter
import matplotlib.pyplot as plt


class MSGService:
    def __init__(self):
        self.messages: dict[str: list[tuple[str: str]]] = {}
        self.unread: dict[str: bool] = {}

    def add_message(self, ch_id: str, author: str, msg: str) -> None:
        if ch_id in self.messages:
            self.messages[ch_id].append((author, msg))
        else:
            self.messages[ch_id] = [(author, msg)]
        self.unread[ch_id] = True
        self.notify_admin_unread()

    def get_channel_messages(self, ch_id: str) -> list[tuple[str: str]] | None:
        if ch_id in self.messages:
            self.unread[ch_id] = False
            return self.messages[ch_id]
        return None

    def notify_admin_unread(self):
        unread_count = sum(self.unread.values())
        if unread_count >= 7:
            print(f"Admin: unread messages in {unread_count} conversations.")

    def generate_most_common_words(self) -> list[tuple[str: int]]:
        all_words = ' '.join([message[1] for messages in self.messages.values() for message in messages]).split()
        word_freq = Counter(all_words)

        common_words = word_freq.most_common(5)  # Display top 5 most common words
        words, freq = zip(*common_words)

        plt.bar(words, freq)
        plt.xlabel('Words')
        plt.ylabel('Count')
        plt.title('Top 5 Most Common Words')
        plt.show()

        return word_freq.most_common(5)
