import collections
import enum
import json
import urllib.request


DEFAULT_VERSION = "v2"


ApiResponse = collections.namedtuple("ApiResponse", ["payload", "status_code"])


class HttpMethods(enum.Enum):
    GET = "GET"
    POST = "POST"


class HttpClient:
    def _request(
        self, url, data=None, headers=None, method=HttpMethods.GET
    ) -> ApiResponse:
        headers = headers or {}
        data = data or {}

        req = urllib.request.Request(
            url, json.dumps(data).encode(), headers, method=method.value
        )
        res = urllib.request.urlopen(req)
        payload = json.loads(res.read().decode())
        return ApiResponse(payload, res.code)

    def get(self, url, headers=None) -> ApiResponse:
        return self._request(url, headers=headers, method=HttpMethods.GET)

    def post(self, url, data=None, headers=None) -> ApiResponse:
        return self._request(url, data, headers=headers, method=HttpMethods.POST)


class NakamaConsoleClient:
    def __init__(self, server_key: str, host: str, port: int = 7351, **kwargs) -> None:
        self.server_key = server_key
        self.host = host
        self.port = port
        self.ssl = kwargs.get("ssl", True)
        self.version = kwargs.get("version", DEFAULT_VERSION)
        self.token = None
        self.http_client = HttpClient()
        self.scheme = "https" if self.ssl else "http"

    def authenticate(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        response = self.http_client.post(
            f"{self.scheme}://{self.host}:{self.port}/{self.version}/console/authenticate",
            data,
        )
        self.token = response.payload["token"]
        return response

    def get_config(self) -> ApiResponse:
        return self.http_client.get(
            f"{self.scheme}://{self.host}:{self.port}/{self.version}/console/config",
            headers={"Authorization": f"Bearer {self.token}"},
        )

    def get_account(self, user_id: str = None):
        url = f"{self.scheme}://{self.host}:{self.port}/{self.version}/console/account"
        if user_id:
            url += f"/{user_id}"

        return self.http_client.get(url, headers={"Authorization": f"Bearer {self.token}"})
