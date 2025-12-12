from enum import auto, Enum
from typing import Type
from requests import get, Response
from gmo_fx.api.api_base import PublicApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.urls import BASE_URL_PUBLIC


class Status(Enum):
    """
    外国為替FXの稼動状態
    """

    OPEN = auto()  # オープン
    CLOSE = auto()  # クローズ
    MAINTENANCE = auto()  # メンテナンス

    @classmethod
    def from_str(cls, text: str) -> Type["Status"]:
        match text:
            case "OPEN":
                return cls.OPEN
            case "CLOSE":
                return cls.CLOSE
            case "MAINTENANCE":
                return cls.MAINTENANCE
        raise ValueError(f"不明なステータスです。: {text}")


class StatusResponse(ResponseBase):
    status: Status

    def __init__(self, response: dict):
        super().__init__(response)
        self.status = Status.from_str(response["data"]["status"])


class StatusApi(PublicApiBase):

    @property
    def _path(self) -> str:
        return f"status"

    @property
    def _method(self) -> PublicApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return StatusResponse

    def _api_error_message(self, response: Response):
        return (
            "ステータスが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
