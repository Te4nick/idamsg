import time
from collections import Counter
from re import sub
import matplotlib.pyplot as plt
from datetime import datetime


class ImageService:
    def __init__(self, image_output_path: str = "./static/png/"):
        self.counter = Counter()
        self.image_output_path = image_output_path + (
            "/" if image_output_path[-1] != "/" else ""
        )

    def put_string(self, msg: str):
        words = list(sub(r"\W+", " ", msg.lower()).split())
        self.counter.update(words)

    def generate_image(self) -> str | None:
        common_words = self.counter.most_common(5)

        if len(common_words) < 5:
            return None

        words, freq = zip(*common_words)

        plt.bar(words, freq)
        plt.xlabel("Words")
        plt.ylabel("Count")
        plt.title("Top 5 Most Common Words")

        time_formatted: str = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        filename: str = f"MostCommonWords_{time_formatted}.png"
        time.sleep(1)  # Imaginary workload. TODO: real workload?
        plt.savefig(self.image_output_path + filename, bbox_inches="tight")

        return self.image_output_path + filename
