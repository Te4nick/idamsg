from datetime import datetime

from src.msg_service import MSGService


def test_add_message():
    ms = MSGService()
    test_table: list[tuple[str, str, str]] = [
        ('prod', 'dev1', 'hi guys'),
        ('prod', 'dev2', 'hello'),
        ('money', 'manager', 'no gold'),
    ]
    for entry in test_table:
        ms.add_message(*entry)

    for test_case in test_table:
        assert (test_case[1], test_case[2]) in ms.messages[test_case[0]]


def test_get_channel_messages():
    ms = MSGService()
    test_table = {
        'prod': [
            ('dev1', 'hi guys'),
            ('dev2', 'hello'),
        ],
        'money': [
            ('manager', 'no gold'),
        ],
    }
    for channel in test_table:
        for msg in test_table[channel]:
            ms.add_message(channel, *msg)

    for test_case in test_table:
        assert ms.get_channel_messages(test_case) == test_table[test_case]

    assert ms.get_channel_messages('dont_exist') is None


def test_notify_admin_unread(capsys):
    ms = MSGService()
    for idx in range(7):
        ms.add_message(f'channel {idx}', f'dev{idx}', f'message {idx}')

    captured = capsys.readouterr()
    assert captured.out == "Admin: unread messages in 7 conversations.\n"


def test_generate_most_common_words():
    ms = MSGService()
    test_table = {
        'prod': [
            ('dev1', 'I am going to drop prod db'),
            ('dev2', 'DONT TOUCH ANYTHING in prod'),
            ('dev3', 'we are fired if prod db goes down'),
            ('dev1', 'BYE BYE'),
            ('dev2', 'dumb dumb'),
        ],
        'money': [
            ('manager', 'where is my money'),
            ('project manager', 'get fired'),
            ('tester', 'wait are you get paid'),
        ],
    }

    for channel in test_table:
        for msg in test_table[channel]:
            ms.add_message(channel, *msg)

    image_path: str = f"./static/png/MostCommonWords_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.png"
    assert ms.generate_most_common_words() == image_path


def test_uninitialized(capsys):
    ms = MSGService()

    ms.notify_admin_unread()
    captured = capsys.readouterr()
    assert captured.out == ""

    assert ms.generate_most_common_words() is None
