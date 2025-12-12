from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal
from requests import get, Response
from gmo_fx.api.api_base import PublicApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Symbol
from gmo_fx.urls import BASE_URL_PUBLIC


@dataclass
class Kline:
    open_time: datetime
    open: float
    high: float
    low: float
    close: float


class KlinesResponse(ResponseBase):
    klines: list[Kline]

    def __init__(self, response: dict):
        super().__init__(response)
        self.klines = []

        data = response["data"]
        self.klines = [
            Kline(
                open=float(d["open"]),
                high=float(d["high"]),
                low=float(d["low"]),
                close=float(d["close"]),
                open_time=datetime.fromtimestamp(int(d["openTime"]) / 1000),
            )
            for d in data
        ]


class KlinesApi(PublicApiBase):
    Symbol = Symbol

    class KlineInterval(Enum):
        Min1 = "1min"
        Min5 = "5min"
        Min10 = "10min"
        Min15 = "15min"
        Min30 = "30min"
        H1 = "1hour"
        H4 = "4hour"
        H8 = "8hour"
        H12 = "12hour"
        D1 = "1day"
        W1 = "1week"
        M1 = "1month"

    @property
    def _path(self) -> str:
        return f"klines"

    @property
    def _method(self) -> PublicApiBase._HttpMethod:
        return self._HttpMethod.GET

    def __call__(
        self,
        symbol: Symbol,
        price_type: Literal["BID", "ASK"],
        interval: KlineInterval,
        date: datetime,
    ) -> KlinesResponse:
        date_str = f"{date.year:04}"
        if interval in (
            self.KlineInterval.Min1,
            self.KlineInterval.Min5,
            self.KlineInterval.Min10,
            self.KlineInterval.Min15,
            self.KlineInterval.Min30,
            self.KlineInterval.H1,
        ):
            date_str += f"{date.month:02}{date.day:02}"

        return super().__call__(
            path_query=f"symbol={symbol.value}"
            f"&priceType={price_type}"
            f"&interval={interval.value}"
            f"&date={date_str}"
        )

    @property
    def _response_parser(self):
        return KlinesResponse

    def _api_error_message(self, response: Response):
        return (
            "Klineが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
