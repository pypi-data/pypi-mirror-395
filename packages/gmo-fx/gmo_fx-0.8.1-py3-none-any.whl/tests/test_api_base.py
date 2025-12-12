import hmac
import hashlib
import json
import pytest
import time
import time_machine
from datetime import datetime
from api.api_base import PrivateApiBase
from api.response import Response
from typing import Any, Optional
from unittest.mock import MagicMock, patch


class PrivateApiBaseStub(PrivateApiBase):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        method: str = "GET",
        body: dict = {},
        path: str = "test",
        is_call: bool = False,
    ) -> None:
        self.__method = (
            self._HttpMethod.POST if method == "POST" else self._HttpMethod.GET
        )
        self.__path = path
        self.__body = body
        self.__is_call = is_call
        super().__init__(api_key, secret_key)

    def __call__(self, *args: Any, **kwds: Any) -> Response:
        if self.__is_call:
            return super().__call__(*args, **kwds)

    @property
    def _response_parser(self):
        return MagicMock()

    @property
    def _path(
        self,
    ) -> str:
        return self.__path

    @property
    def _body(
        self,
    ) -> str:
        return self.__body

    @property
    def _method(self):
        return self.__method

    @property
    def header(
        self,
    ) -> dict:
        return super()._create_header()


class TestPrivateApiBase:

    def test_api_key_header(self):
        header = PrivateApiBaseStub(api_key="api_key", secret_key="secret").header
        assert header["API-KEY"] == "api_key"

    bodys = [
        # (body, expect),
        (None, None),
        ({}, "{}"),
        ({"test": "test"}, '{"test":"test"}'),
        ({"test": ""}, '{"test":""}'),
    ]

    @pytest.mark.parametrize(
        "body, expect",
        bodys,
    )
    @patch("api.api_base.post")
    def test_should_post_with_body(
        self,
        post_mock: MagicMock,
        body: Optional[dict],
        expect: Optional[str],
    ):
        respose = MagicMock()
        respose.status_code = 200
        respose.json.return_value = {}
        post_mock.return_value = respose
        api = PrivateApiBaseStub(
            api_key="api_key",
            secret_key="secret",
            body=body,
            method="POST",
            is_call=True,
        )
        api(data=body)
        post_mock.assert_called_once()
        kall = post_mock.call_args
        expect = (
            expect.replace(":", ": ") if expect else None
        )  # FIXME: 定義でスペースを空けるとテストがエラーになる
        assert kall.kwargs["data"] == expect
        assert api._body == body

    @time_machine.travel(datetime(2022, 12, 25))
    def test_timestamp(self):
        header = PrivateApiBaseStub(api_key="api_key", secret_key="secret").header
        assert header["API-TIMESTAMP"] == "{0}000".format(
            int(time.mktime(datetime.now().timetuple()))
        )

    @time_machine.travel(datetime(2024, 1, 3))
    def test_api_sign_get(self):
        method = "GET"
        path = "test"
        body = {"a": "a"}
        header = PrivateApiBaseStub(
            api_key="api_key", secret_key="secret", method=method, path=path, body=body
        ).header
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = timestamp + method + f"/{PrivateApiBaseStub.VERSION}/{path}"
        assert (
            header["API-SIGN"]
            == hmac.new(
                bytes("secret".encode("ascii")),
                bytes(text.encode("ascii")),
                hashlib.sha256,
            ).hexdigest()
        )

    @time_machine.travel(datetime(2024, 1, 3))
    def test_api_sign_post(self):
        method = "POST"
        path = "test"
        body = {"a": "a"}
        header = PrivateApiBaseStub(
            api_key="api_key", secret_key="secret", method=method, path=path, body=body
        ).header
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = (
            timestamp
            + method
            + f"/{PrivateApiBaseStub.VERSION}/{path}"
            + json.dumps(body)
        )
        assert (
            header["API-SIGN"]
            == hmac.new(
                bytes("secret".encode("ascii")),
                bytes(text.encode("ascii")),
                hashlib.sha256,
            ).hexdigest()
        )
