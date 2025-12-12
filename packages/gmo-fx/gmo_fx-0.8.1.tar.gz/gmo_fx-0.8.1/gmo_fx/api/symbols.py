from dataclasses import dataclass
from enum import Enum
from gmo_fx.api.api_base import PublicApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Symbol
from requests import get, Response
from gmo_fx.urls import BASE_URL_PUBLIC


@dataclass
class Rule:
    Symbol = Symbol
    symbol: Symbol
    min_open_order_size: int
    max_order_size: int
    size_step: int
    tick_size: float


class SymbolsResponse(ResponseBase):
    rules: list[Rule]

    def __init__(self, response: dict):
        super().__init__(response)
        self.rules = []

        data = response["data"]
        self.rules = [
            Rule(
                symbol=Rule.Symbol(d["symbol"]),
                min_open_order_size=int(d["minOpenOrderSize"]),
                max_order_size=int(d["maxOrderSize"]),
                size_step=int(d["sizeStep"]),
                tick_size=float(d["tickSize"]),
            )
            for d in data
        ]


class SymbolsApi(PublicApiBase):

    @property
    def _path(self) -> str:
        return f"symbols"

    @property
    def _method(self) -> PublicApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return SymbolsResponse

    def _api_error_message(self, response: Response):
        return (
            "取引ルールが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
