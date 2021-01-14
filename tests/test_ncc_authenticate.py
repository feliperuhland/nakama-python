import nakama

import pytest


@pytest.fixture
def client():
    return nakama.NakamaConsoleClient("defaultkey", "127.0.0.1", ssl=False)


@pytest.fixture
def client_admin(client):
    client.authenticate("admin", "password")
    return client


def test_ncc_authenticate(client):
    response = client.authenticate("admin", "password")
    assert 100 < len(response.payload["token"])


def test_ncc_config(client_admin):
    response = client_admin.get_config()
    assert "config" in response.payload


def test_get_account(client_admin):
    response = client_admin.get_account()
    assert response.payload["users"]

    user_id = "00000000-0000-0000-0000-000000000000"
    response = client_admin.get_account(user_id)
    assert user_id == response.payload["account"]["user"]["id"]
