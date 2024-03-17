from datetime import datetime

from core.msg.services import ImageService
from collections import Counter


def test_put_string_valid():
    test_table = {
        "input": {
            "msg": "one 1 two 2 three 3 four 4 five 5 I go seek",
        },
        "result": {
            "counter": Counter(
                [
                    "one",
                    "1",
                    "two",
                    "2",
                    "three",
                    "3",
                    "four",
                    "4",
                    "five",
                    "5",
                    "i",
                    "go",
                    "seek",
                ]
            )
        },
    }
    service = ImageService()
    service.put_string(test_table["input"]["msg"])
    assert service.counter == test_table["result"]["counter"]


def test_put_string_empty():
    test_table = {
        "input": {
            "msg": "",
        },
        "result": {
            "counter": Counter(),
        },
    }
    service = ImageService()
    service.put_string(test_table["input"]["msg"])
    assert service.counter == test_table["result"]["counter"]


def test_generate_image_valid():
    time_formatted: str = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    filename: str = f"MostCommonWords_{time_formatted}.png"
    path: str = f"./static/png/{filename}"
    test_table = {
        "input": {
            # "image_output_path": "./../static/img",
            "counter": Counter(
                [
                    "1",
                    "2",
                    "2",
                    "3",
                    "3",
                    "3",
                    "4",
                    "4",
                    "4",
                    "4",
                    "5",
                    "5",
                    "5",
                    "5",
                    "5",
                ]
            ),
        },
        "result": {
            "path": path,
        },
    }
    service = ImageService()
    service.counter = test_table["input"]["counter"]
    assert service.generate_image() == test_table["result"]["path"]


def test_generate_image_not_enough_words():
    test_table = {
        "input": {
            # "image_output_path": "./../static/img",
            "counter": Counter(
                [
                    "1",
                    "2",
                    "2",
                    "3",
                    "3",
                    "3",
                    "4",
                    "4",
                    "4",
                    "4",
                ]
            ),
        },
        "result": {
            "path": None,
        },
    }
    service = ImageService()
    service.counter = test_table["input"]["counter"]
    assert service.generate_image() == test_table["result"]["path"]
