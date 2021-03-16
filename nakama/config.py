import urllib.parse


DEFAULT_VERSION = "v2"


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
