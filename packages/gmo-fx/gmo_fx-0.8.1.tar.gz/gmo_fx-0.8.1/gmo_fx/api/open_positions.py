from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Side, Symbol


@dataclass
class OpenPosition:
    Side = Side
    Symbol = Symbol

    position_id: int
    symbol: Symbol
    side: Side
    size: int
    ordered_size: int
    price: float
    loss_gain: float
    total_swap: float
    timestamp: datetime


class OpenPositionsResponse(ResponseBase):
    open_positions: list[OpenPosition]

    def __init__(self, response: dict):
        super().__init__(response)
        self.open_positions = []

        data = response["data"]["list"]
        self.open_positions = [
            OpenPosition(
                position_id=d["positionId"],
                symbol=OpenPosition.Symbol(d["symbol"]),
                side=OpenPosition.Side(d["side"]),
                size=int(d["size"]),
                ordered_size=int(d["orderedSize"]),
                price=float(d["price"]),
                loss_gain=float(d["lossGain"]),
                total_swap=float(d["totalSwap"]),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
            )
            for d in data
        ]


class OpenPositionsApi(PrivateApiBase):
    Symbol = Symbol

    @property
    def _path(self) -> str:
        return "openPositions"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return OpenPositionsResponse

    def _api_error_message(self, response: Response):
        return (
            "建玉一覧が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Optional[Symbol] = None,
        prev_id: Optional[int] = None,
        count: Optional[int] = None,
    ) -> OpenPositionsResponse:
        path_query = ""
        if symbol:
            path_query = f"symbol={symbol.value}"

        if prev_id:
            if path_query:
                path_query += "&"
            path_query = f"prevId={prev_id}"

        if count:
            if path_query:
                path_query += "&"
            path_query = f"count={count}"

        return super().__call__(path_query=path_query)
