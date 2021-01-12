import nakama

import pytest


@pytest.fixture
def ncc():
    return nakama.NakamaConsoleClient("defaultkey", "127.0.0.1")


def test_ncc_authenticate(ncc):
    token = ncc.authenticate("admin", "password")
    assert 100 < len(token)


def test_ncc_config(ncc):
    ncc.authenticate("admin", "password")
    config = ncc.config()

    assert "config" in config
