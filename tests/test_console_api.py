import http

import pytest

import nakama.api
import nakama.types


def clean_user_data(client):
    res = client.users.get()
    for user in res.payload.get("users"):
        client.users.remove(user.get("username"))


@pytest.fixture
def noauth_client():
    return nakama.api.NakamaConsoleApi(server_key="defaultkey", host="127.0.0.1", ssl=False)


@pytest.fixture
def client(noauth_client: nakama.api.NakamaConsoleApi):
    noauth_client.authenticate("admin", "password")
    clean_user_data(noauth_client)
    return noauth_client


def test_ncc_authenticate(noauth_client):
    response = noauth_client.authenticate("admin", "password")
    assert 100 < len(response.payload["token"])


def test_ncc_config(client):
    response = client.config.get()
    assert "config" in response.payload


def test_ncc_status(client):
    response = client.status.get()
    assert "nodes" in response.payload
    assert "timestamp" in response.payload
    assert "nakama1" in response.payload.get("nodes", [])[0].get("name")


def test_get_account(client):
    response = client.accounts.get()
    assert response.payload["users"]

    user_id = "00000000-0000-0000-0000-000000000000"
    response = client.accounts.get(user_id)
    assert user_id == response.payload["account"]["user"]["id"]


def test_post_console_user(client):
    username = "user1"
    password = "Passwd1"
    email = "email1@email.com"
    role = nakama.types.RoleEnum.USER_ROLE_READONLY.value

    response = client.users.create(username, password, email, role)
    assert {} == response.payload
    assert http.HTTPStatus.OK == response.status_code


def test_delete_console_user_not_found(client):
    username = "user1"
    password = "Passwd1"
    email = "email1@email.com"
    role = nakama.types.RoleEnum.USER_ROLE_READONLY.value

    client.users.create(username, password, email, role)
    response = client.users.remove(username)
    assert {} == response.payload
    assert http.HTTPStatus.OK == response.status_code


def test_delete_console_user(client):
    username = "user1"
    response = client.users.remove(username)
    assert "User not found" == response.payload.get("message")
    assert http.HTTPStatus.BAD_REQUEST == response.status_code


def test_get_console_endpoints(client):
    response = client.endpoints.get()
    assert http.HTTPStatus.OK == response.status_code
    assert "endpoints" in response.payload
    assert "rpc_endpoints" in response.payload


def test_get_console_runtime(client):
    response = client.runtime.get()
    assert http.HTTPStatus.OK == response.status_code
    assert "go_rpc_functions" in response.payload
    assert "go_modules" in response.payload
    assert "lua_rpc_functions" in response.payload
    assert "lua_modules" in response.payload
    assert "js_rpc_functions" in response.payload
    assert "js_modules" in response.payload
