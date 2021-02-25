import collections
import json
import urllib.request
import urllib.parse

import nakama.types


DEFAULT_VERSION = "v2"


ApiResponse = collections.namedtuple("ApiResponse", ["payload", "status_code"])


class NakamaConfig:
    def __init__(self, server_key: str, host: str, **kwargs) -> None:
        self.server_key = server_key
        self.host = host
        self.port = int(kwargs.get("port", 7351))
        self.ssl = kwargs.get("ssl", True)
        self.version = kwargs.get("version", DEFAULT_VERSION)
        self.token = None
        self.scheme = "https" if self.ssl else "http"

    def build_url(self, path: str = "") -> str:
        return urllib.parse.urljoin(
            f"{self.scheme}://{self.host}:{self.port}/{self.version}/", path
        )

    @property
    def auth_header(self):
        return {"Authorization": f"Bearer {self.token}"}


class HttpClient:
    def _request(
        self, url, data=None, headers=None, method=nakama.types.HttpMethods.GET
    ) -> ApiResponse:
        headers = headers or {}
        data = data or {}

        req = urllib.request.Request(url, json.dumps(data).encode(), headers, method=method.value)
        try:
            res = urllib.request.urlopen(req)
            payload = json.loads(res.read().decode())
            status_code = res.code
        except urllib.error.HTTPError as exc:
            payload = json.loads(exc.file.read().decode())
            status_code = exc.code
        return ApiResponse(payload, status_code)

    def delete(self, url, headers=None) -> ApiResponse:
        return self._request(url, headers=headers, method=nakama.types.HttpMethods.DELETE)

    def get(self, url, headers=None) -> ApiResponse:
        return self._request(url, headers=headers, method=nakama.types.HttpMethods.GET)

    def post(self, url, headers=None, data=None) -> ApiResponse:
        return self._request(url, data, headers=headers, method=nakama.types.HttpMethods.POST)


class AccountClient:
    def __init__(self, http_client: HttpClient, nakama_config: NakamaConfig):
        self.http_client = http_client
        self.nakama_config = nakama_config

    def get(self, user_id: str = None) -> ApiResponse:
        url = f"account/{user_id}" if user_id else "account"
        return self.http_client.get(
            self.nakama_config.build_url(f"console/{url}"), self.nakama_config.auth_header
        )


class ConfigClient:
    def __init__(self, http_client: HttpClient, nakama_config: NakamaConfig):
        self.http_client = http_client
        self.nakama_config = nakama_config

    def get(self) -> ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/config"), self.nakama_config.auth_header
        )


class StatusClient:
    def __init__(self, http_client: HttpClient, nakama_config: NakamaConfig):
        self.http_client = http_client
        self.nakama_config = nakama_config

    def get(self) -> ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/status"), self.nakama_config.auth_header
        )


class UserClient:
    def __init__(self, http_client: HttpClient, nakama_config: NakamaConfig):
        self.http_client = http_client
        self.nakama_config = nakama_config

    def create(self, username: str, password: str, email: str, role: str) -> ApiResponse:
        payload = dict(username=username, password=password, email=email, role=role)
        return self.http_client.post(
            self.nakama_config.build_url("console/user"),
            self.nakama_config.auth_header,
            payload,
        )

    def get(self, username: str = None, email: str = None, role: str = None) -> ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/user"),
            self.nakama_config.auth_header,
        )

    def remove(self, username: str) -> ApiResponse:
        return self.http_client.delete(
            self.nakama_config.build_url(f"console/user?username={username}"),
            self.nakama_config.auth_header,
        )


class NakamaConsoleClient:
    def __init__(self, **kwargs) -> None:
        self.nakama_config = NakamaConfig(**kwargs)
        self.http_client = HttpClient()

    @property
    def accounts(self):
        return AccountClient(self.http_client, self.nakama_config)

    @property
    def config(self):
        return ConfigClient(self.http_client, self.nakama_config)

    @property
    def status(self):
        return StatusClient(self.http_client, self.nakama_config)

    @property
    def users(self):
        return UserClient(self.http_client, self.nakama_config)

    def authenticate(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        response = self.http_client.post(
            self.nakama_config.build_url("console/authenticate"),
            data=data,
        )
        self.nakama_config.token = response.payload["token"]
        return response
