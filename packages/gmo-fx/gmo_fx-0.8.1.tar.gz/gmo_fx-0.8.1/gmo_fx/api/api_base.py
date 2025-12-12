import hmac
import hashlib
import json
import time

from abc import ABC, abstractmethod
from datetime import datetime
from enum import auto, Enum
from gmo_fx.api.response import Response as ApiResponse
from requests import get, post, Response
from typing import Any, Optional, Type


class ApiBase(ABC):

    class _HttpMethod(Enum):
        GET = "GET"
        POST = "POST"

    VERSION = "v1"

    @property
    @abstractmethod
    def _path(self) -> str:
        pass

    @property
    @abstractmethod
    def _method(self) -> _HttpMethod:
        pass

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        pass

    @property
    def _body(self) -> dict:
        return getattr(self, "_request_body", {})

    def __call__(self, *args: Any, **kwds: Any) -> ApiResponse:

        response: Response = self._call_api(*args, **kwds)
        if response.status_code == 200:
            response_json = response.json()
            return self._response_parser(response_json)

        raise RuntimeError(self._api_error_message(response))

    @property
    def _response_parser(self) -> Type[ApiResponse]:
        pass

    def _api_error_message(self, response: Response):
        return (
            "APIの実行に失敗しました。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def _create_header(
        self,
    ) -> dict:
        return {}

    def _call_api(
        self, path_query: Optional[str] = None, data: Optional[dict] = None
    ) -> Response:
        url = f"{self._endpoint}/{self.VERSION}/{self._path}"
        if path_query:
            url += f"?{path_query}"
        if self._method == self._HttpMethod.GET:
            return get(
                url,
                headers=self._create_header(),
            )
        elif self._method == self._HttpMethod.POST:
            req_body = None
            if data is not None:
                self._request_body = data
                req_body = json.dumps(data)

            return post(url, headers=self._create_header(), data=req_body)
        raise ValueError


class PublicApiBase(ApiBase, ABC):
    @property
    def _endpoint(self) -> str:
        return "https://forex-api.coin.z.com/public"


class PrivateApiBase(ApiBase, ABC):
    def __init__(self, api_key: str, secret_key: str) -> None:
        self._api_key = api_key
        self.__secret_key = secret_key
        super().__init__()

    @property
    def _endpoint(self) -> str:
        return "https://forex-api.coin.z.com/private"

    def _create_header(
        self,
    ) -> dict:
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = timestamp + self._method.value + "/" + self.VERSION + "/" + self._path
        if self._method == self._HttpMethod.POST:
            text += json.dumps(self._body)
        sign = hmac.new(
            bytes(self.__secret_key.encode("ascii")),
            bytes(text.encode("ascii")),
            hashlib.sha256,
        ).hexdigest()
        return {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign,
        }
