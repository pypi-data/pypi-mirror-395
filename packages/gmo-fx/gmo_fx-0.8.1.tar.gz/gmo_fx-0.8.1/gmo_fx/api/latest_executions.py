from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import SettleType, Side, Symbol


@dataclass
class Execution:
    Symbol = Symbol
    Side = Side
    SettleType = SettleType

    amount: float
    execution_id: int
    client_order_id: str
    order_id: int
    position_id: int
    symbol: Symbol
    side: Side
    settle_type: SettleType
    size: int
    price: float
    loss_gain: int
    fee: int
    settled_swap: float
    timestamp: datetime


class LatestExecutionsResponse(ResponseBase):
    executions: list[Execution]

    def __init__(self, response: dict):
        super().__init__(response)
        self.assets = []

        data = response["data"]["list"]
        self.executions = [
            Execution(
                amount=float(d["amount"]),
                execution_id=d["executionId"],
                client_order_id=d["clientOrderId"],
                order_id=d["orderId"],
                position_id=d["positionId"],
                symbol=Symbol(d["symbol"]),
                side=Side(d["side"]),
                settle_type=SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d["price"]),
                loss_gain=int(d["lossGain"]),
                fee=int(d["fee"]),
                settled_swap=float(d["settledSwap"]),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
            )
            for d in data
        ]


class LatestExecutionsApi(PrivateApiBase):
    Symbol = Symbol

    @property
    def _path(self) -> str:
        return "latestExecutions"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return LatestExecutionsResponse

    def _api_error_message(self, response: Response):
        return (
            "最新約定一覧が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Symbol,
        count: int = 100,
    ) -> LatestExecutionsResponse:
        return super().__call__(path_query=f"symbol={symbol.value}" f"&count={count}")
