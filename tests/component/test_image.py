import http
import requests

BASE_URL = "http://localhost:8000"
VALID_IMAGE_UUID = ""


def test_get_image_generate_valid():
    test_table = {
        "input": {
            "data": {
                "channel_id": "image",
                "author": "/dev/null",
                "content": "1 2 2 3 3 3 4 4 4 4 5 5 5 5 5",
            },
        },
    }
    response = requests.post(
        url=f"{BASE_URL}/messages",
        json=test_table["input"]["data"],
    )
    assert response.status_code == http.HTTPStatus.CREATED

    response = requests.get(url=f"{BASE_URL}/image/generate")
    assert response.status_code == http.HTTPStatus.OK
    response_data = response.json()
    assert response_data["done"] is False

    global VALID_IMAGE_UUID  # saving results and cleaning up
    VALID_IMAGE_UUID = response_data["id"]
    response = requests.get(
        url=f"{BASE_URL}/messages?channel_id=image",
    )
    assert response.status_code == http.HTTPStatus.OK


def test_get_image_status_valid():
    global VALID_IMAGE_UUID  # get operation uuid from previous test

    response = requests.get(
        url=f"{BASE_URL}/image/status?id={VALID_IMAGE_UUID}"
    )  # may need more time before launch
    assert response.status_code == http.HTTPStatus.OK
    response_data = response.json()
    assert response_data["done"] is True


def test_get_image_status_not_found():
    test_table = {
        "input": {
            "id": "550e8400-e29b-41d4-a716-446655440000",  # https://en.wikipedia.org/wiki/Universally_unique_identifier
        },
        "result": {
            "status": http.HTTPStatus.NOT_FOUND,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/image/status?id={test_table['input']['id']}"
    )  # may need more time before launch
    assert response.status_code == test_table["result"]["status"]


def test_get_image_status_unprocessable_entity():
    test_table = {
        "input": {
            "id": "should_be_correct_format_and_36_char",
        },
        "result": {
            "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    }
    response = requests.get(
        url=f"{BASE_URL}/image/status?id={test_table['input']['id']}"
    )  # may need more time before launch
    assert response.status_code == test_table["result"]["status"]
