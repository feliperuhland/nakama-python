import enum
import json
import urllib.request


DEFAULT_VERSION = 2


class HttpMethods(enum.Enum):
    GET = "GET"
    POST = "POST"


class NakamaConsoleClient:
    def __init__(self, server_key: str, host: str, port: int = 7351, **kwargs) -> None:
        self.server_key = server_key
        self.host = host
        self.port = port
        self.ssl = kwargs.get("ssl", True)
        self.version = kwargs.get("version", DEFAULT_VERSION)
        self.token = None

    def _http_request(self, url, data, headers=None, method=HttpMethods.GET):
        headers = headers or {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        req = urllib.request.Request(url, json.dumps(data).encode(), headers, method=method.value)
        res = urllib.request.urlopen(req)
        payload = json.loads(res.read().decode())
        return payload

    def authenticate(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        payload = self._http_request(
            f"http://{self.host}:{self.port}/v2/console/authenticate",
            data,
            method=HttpMethods.POST,
        )
        self.token = payload["token"]
        return self.token

    def config(self):
        payload = self._http_request(
            f"http://{self.host}:{self.port}/v2/console/config",
            {},
            method=HttpMethods.GET,
        )
        return payload
