import json
import urllib.request

import nakama.types


class HttpClient:
    def _request(
        self, url, data=None, headers=None, method=nakama.types.HttpMethods.GET
    ) -> nakama.types.ApiResponse:
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
        return nakama.types.ApiResponse(payload, status_code)

    def delete(self, url, headers=None) -> nakama.types.ApiResponse:
        return self._request(url, headers=headers, method=nakama.types.HttpMethods.DELETE)

    def get(self, url, headers=None) -> nakama.types.ApiResponse:
        return self._request(url, headers=headers, method=nakama.types.HttpMethods.GET)

    def post(self, url, headers=None, data=None) -> nakama.types.ApiResponse:
        return self._request(url, data, headers=headers, method=nakama.types.HttpMethods.POST)
