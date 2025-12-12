from dataclasses import dataclass
from enum import Enum
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Side, Symbol


@dataclass
class Position:
    Side = Side
    Symbol = Symbol

    average_position_rate: float
    position_loss_gain: float
    side: Side
    sum_ordered_size: int
    sum_position_size: int
    sum_total_swap: float
    symbol: Symbol


class PositionSummaryResponse(ResponseBase):
    positions: list[Position]

    def __init__(self, response: dict):
        super().__init__(response)
        self.assets = []

        data = response["data"]["list"]
        self.positions = [
            Position(
                average_position_rate=float(d["averagePositionRate"]),
                position_loss_gain=float(d["positionLossGain"]),
                side=Position.Side(d["side"]),
                sum_ordered_size=int(d["sumOrderedSize"]),
                sum_position_size=int(d["sumPositionSize"]),
                sum_total_swap=float(d["sumTotalSwap"]),
                symbol=Position.Symbol(d["symbol"]),
            )
            for d in data
        ]


class PositionSummaryApi(PrivateApiBase):
    Symbol = Symbol

    @property
    def _path(self) -> str:
        return "positionSummary"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return PositionSummaryResponse

    def _api_error_message(self, response: Response):
        return (
            "建玉サマリーが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Symbol,
    ) -> PositionSummaryResponse:
        return super().__call__(path_query=f"symbol={symbol.value}")
