import abc

import nakama.client
import nakama.config
import nakama.types


class BaseApi(abc.ABC):
    def __init__(
        self, http_client: nakama.client.HttpClient, nakama_config: nakama.config.NakamaConfig
    ):
        self.http_client = http_client
        self.nakama_config = nakama_config


class AccountApi(BaseApi):
    def get(self, user_id: str = None) -> nakama.types.ApiResponse:
        url = f"account/{user_id}" if user_id else "account"
        return self.http_client.get(
            self.nakama_config.build_url(f"console/{url}"), self.nakama_config.auth_header
        )


class ConfigApi(BaseApi):
    def get(self) -> nakama.types.ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/config"), self.nakama_config.auth_header
        )


class EndpointsApi(BaseApi):
    def get(self) -> nakama.types.ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/api/endpoints"), self.nakama_config.auth_header
        )


class RuntimeApi(BaseApi):
    def get(self) -> nakama.types.ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/runtime"), self.nakama_config.auth_header
        )


class StatusApi(BaseApi):
    def get(self) -> nakama.types.ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/status"), self.nakama_config.auth_header
        )


class UserApi(BaseApi):
    def create(
        self, username: str, password: str, email: str, role: str
    ) -> nakama.types.ApiResponse:
        payload = dict(username=username, password=password, email=email, role=role)
        return self.http_client.post(
            self.nakama_config.build_url("console/user"),
            self.nakama_config.auth_header,
            payload,
        )

    def get(
        self, username: str = None, email: str = None, role: str = None
    ) -> nakama.types.ApiResponse:
        return self.http_client.get(
            self.nakama_config.build_url("console/user"),
            self.nakama_config.auth_header,
        )

    def remove(self, username: str) -> nakama.types.ApiResponse:
        return self.http_client.delete(
            self.nakama_config.build_url(f"console/user?username={username}"),
            self.nakama_config.auth_header,
        )


class NakamaConsoleApi:
    def __init__(self, **kwargs) -> None:
        self.nakama_config = nakama.config.NakamaConfig(**kwargs)
        self.http_client = nakama.client.HttpClient()

    @property
    def accounts(self):
        return AccountApi(self.http_client, self.nakama_config)

    @property
    def config(self):
        return ConfigApi(self.http_client, self.nakama_config)

    @property
    def endpoints(self):
        return EndpointsApi(self.http_client, self.nakama_config)

    @property
    def runtime(self):
        return RuntimeApi(self.http_client, self.nakama_config)

    @property
    def status(self):
        return StatusApi(self.http_client, self.nakama_config)

    @property
    def users(self):
        return UserApi(self.http_client, self.nakama_config)

    def authenticate(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        response = self.http_client.post(
            self.nakama_config.build_url("console/authenticate"),
            data=data,
        )
        self.nakama_config.token = response.payload["token"]
        return response
