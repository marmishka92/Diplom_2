import pytest
import requests
from data import UrlsApi
from helpers import UserData

@pytest.fixture(autouse=True)
def create_new_user():

    payload = UserData.create_user_data()

    response = requests.post(UrlsApi.CREATE_USER, json=payload)
    yield payload, response

    try:
        token = response.json().get("accessToken")
        if token:
            requests.delete(UrlsApi.DELETE_USER, headers={"Authorization": token})
    except Exception:
        pass
