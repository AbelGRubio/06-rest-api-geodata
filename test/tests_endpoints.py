import json
import os
import random

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from api_module.functions import exist_user

from src.__main__ import APP

load_dotenv()

EXIST_USER_MSG = os.getenv("EXIST_USER_MSG")
ADDED_USER_MSG = os.getenv("ADDED_USER_MSG")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = TestClient(APP)


def is_json(myjson: bytes):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def test_is_json_api():
    response = client.post(
        "/add_user",
        json={
            "user": "user{}".format(int(random.random() * 1000)),
            "postal_code": "26005"
        }
    )
    assert is_json(response.content), \
        "The response is not json format!"

    return True


def test_add_user_api():
    response = client.post(
        "/add_user",
        json={
            "user": "user{}".format(int(random.random() * 1000)),
            "postal_code": "26005"
        }
    )
    msg = response.json()['msg']

    assert msg == ADDED_USER_MSG, \
        "The message to add user was: {}!".format(msg)

    return True


def test_add_same_user_twice_api():
    if not exist_user(DATABASE_NAME, "user200"):
        response = client.post(
            "/add_user",
            json={
                "user": "user200",
                "postal_code": "26005"
            }
        )

    response = client.post(
        "/add_user",
        json={
            "user": "user200",
            "postal_code": "26005"
        }
    )
    msg = response.json()['msg']

    assert msg == EXIST_USER_MSG, \
        "The message to add same user was: {}!".format(msg)

    return True
