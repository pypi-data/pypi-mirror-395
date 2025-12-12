from dataclasses import dataclass
from datetime import datetime
from requests import get, Response
from gmo_fx.api.api_base import PublicApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Symbol
from gmo_fx.urls import BASE_URL_PUBLIC


@dataclass
class Ticker:
    Symbol = Symbol
    symbol: Symbol
    ask: float
    bid: float
    timestamp: datetime
    status: str


class TickerResponse(ResponseBase):
    tickers: list[Ticker]

    def __init__(self, response: dict):
        super().__init__(response)
        self.tickers = []

        data = response["data"]
        self.tickers = [
            Ticker(
                symbol=Ticker.Symbol(d["symbol"]),
                ask=d["ask"],
                bid=d["bid"],
                status=d["status"],
                timestamp=datetime.strptime(d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            )
            for d in data
        ]


class TickerApi(PublicApiBase):

    @property
    def _path(self) -> str:
        return f"ticker"

    @property
    def _method(self) -> PublicApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return TickerResponse

    def _api_error_message(self, response: Response):
        return (
            "最新レートが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
