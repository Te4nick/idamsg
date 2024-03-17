from core.msg.services import MSGService
from core.msg.models import Message


def test_message_creation_valid() -> None:
    test_table = {
        "input": {
            "channel_id": "prod",
            "author": "/dev/null",
            "content": "testing stuff",
        },
        "result": {
            "messages": {
                "prod": [
                    Message(
                        "/dev/null",
                        "testing stuff",
                    )
                ]
            },
            "unread_channels": {
                "prod": True,
            },
        },
    }
    service = MSGService()
    service.add_message(
        channel_id=test_table["input"]["channel_id"],
        author=test_table["input"]["author"],
        content=test_table["input"]["content"],
    )
    assert (
        service.messages == test_table["result"]["messages"]
        and service.unread_channels == test_table["result"]["unread_channels"]
    )


def test_get_channel_messages_valid() -> None:
    test_table = {
        "input": {
            "messages": {
                "prod": [
                    Message("/dev/null", "testing stuff"),
                    Message("/dev/null", "testing stuff 2"),
                ],
            },
            "unread_channels": {
                "prod": True,
            },
            "channel_id": "prod",
        },
        "result": {
            "messages": [
                Message("/dev/null", "testing stuff"),
                Message("/dev/null", "testing stuff 2"),
            ],
            "unread_channels": {},
        },
    }
    service = MSGService()
    service.messages = test_table["input"]["messages"]
    service.unread_channels = test_table["input"]["unread_channels"]

    assert (
        service.get_channel_messages(test_table["input"]["channel_id"])
        == test_table["result"]["messages"]
        and service.unread_channels == test_table["result"]["unread_channels"]
    )


def test_get_channel_messages_nonexistent_channel_id() -> None:
    test_table = {
        "input": {
            "channel_id": "prod",
        },
        "result": {"messages": None},
    }
    service = MSGService()

    assert (
        service.get_channel_messages(test_table["input"]["channel_id"])
        == test_table["result"]["messages"]
    )


def test_notify_admin_unread_unread_channels_equals_7() -> None:
    test_table = {
        "input": {
            "unread_channels": {
                "prod": True,
                "dev": True,
                "design": True,
                "test": True,
                "devops": True,
                "sre": True,
                "features": True,
            },
        },
        "result": [
            "prod",
            "dev",
            "design",
            "test",
            "devops",
            "sre",
            "features",
        ],
    }
    service = MSGService()
    service.unread_channels = test_table["input"]["unread_channels"]

    assert service.notify_admin_unread() == test_table["result"]


def test_notify_admin_unread_unread_channels_empty() -> None:
    test_table = {
        "input": {
            "unread_channels": {},
        },
        "result": None,
    }
    service = MSGService()
    service.unread_channels = test_table["input"]["unread_channels"]

    assert service.notify_admin_unread() == test_table["result"]
