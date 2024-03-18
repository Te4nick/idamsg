import http
import requests

BASE_URL = "http://localhost:8000"


def test_post_message_valid():
    test_table = {
        "input": {
            "data": {
                "channel_id": "prod",
                "author": "/dev/null",
                "content": "testing stuff",
            },
        },
        "result": {
            "data": {
                "author": "/dev/null",
                "content": "testing stuff",
                "channel_id": "prod",
            },
            "status": http.HTTPStatus.CREATED,
        },
    }
    response = requests.post(
        url=f"{BASE_URL}/messages",
        json=test_table["input"]["data"],
    )
    assert response.status_code == test_table["result"]["status"]
    response_data = response.json()
    assert response_data == test_table["result"]["data"]


def test_post_message_unprocessable_entity():
    test_table = {
        "input": {
            "data": {
                "author": "/dev/null",
                "content": "testing stuff",
            },
        },
        "result": {
            "data": {
                "channel_id": [
                    "This field is required.",
                ],
            },
            "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    }
    response = requests.post(
        url=f"{BASE_URL}/messages",
        json=test_table["input"]["data"],
    )
    assert response.status_code == test_table["result"]["status"]
    response_data = response.json()
    assert response_data == test_table["result"]["data"]


def test_get_messages_valid():  # assuming previous tests ran before this
    test_table = {
        "input": {},
        "result": {
            "data": [
                {
                    "author": "/dev/null",
                    "content": "testing stuff",
                },
            ],
            "status": http.HTTPStatus.OK,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/messages?channel_id=prod",
    )
    assert response.status_code == test_table["result"]["status"]
    response_data = response.json()
    assert response_data == test_table["result"]["data"]


def test_get_messages_channel_not_found():
    test_table = {
        "input": {},
        "result": {
            "status": http.HTTPStatus.NOT_FOUND,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/messages?channel_id=NONEXIST",
    )
    assert response.status_code == test_table["result"]["status"]


def test_get_messages_unprocessable_entity():
    test_table = {
        "input": {},
        "result": {
            "data": {
                "channel_id": [
                    "This field is required.",
                ],
            },
            "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/messages",
    )
    assert response.status_code == test_table["result"]["status"]
    response_data = response.json()
    assert response_data == test_table["result"]["data"]


def test_get_messages_unread_no_content():
    test_table = {
        "input": {},
        "result": {
            "status": http.HTTPStatus.NO_CONTENT,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/messages/unread",
    )
    assert response.status_code == test_table["result"]["status"]


def test_get_messages_unread_valid():
    test_table = {
        "input": {
            "data": [],
        },
        "result": {
            "data": [],
            "status": http.HTTPStatus.OK,
        },
    }
    for i in range(7):
        workload = {
            "channel_id": f"dev{i}",
            "author": "/dev/null",
            "content": "testing stuff",
        }
        test_table["result"]["data"].append({"id": f"dev{i}"})
        response = requests.post(
            url=f"{BASE_URL}/messages",
            json=workload,
        )
        assert response.status_code == http.HTTPStatus.CREATED

    response = requests.get(
        url=f"{BASE_URL}/messages/unread",
    )
    assert response.status_code == test_table["result"]["status"]
    response_data = response.json()
    assert response_data == test_table["result"]["data"]
