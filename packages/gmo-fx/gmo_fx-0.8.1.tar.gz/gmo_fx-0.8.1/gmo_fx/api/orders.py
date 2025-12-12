from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Side, Symbol, SettleType


@dataclass
class Order:
    class OrderType(Enum):
        NORMAL = "NORMAL"
        OCO = "OCO"
        IFD = "IFD"
        IFDOCO = "IFDOCO"
        LOSSCUT = "LOSSCUT"

    class ExecutionType(Enum):
        MARKET = "MARKET"
        LIMIT = "LIMIT"
        STOP = "STOP"

    class Status(Enum):
        WAITING = "WAITING"
        ORDERED = "ORDERED"
        MODIFYING = "MODIFYING"
        CANCELED = "CANCELED"
        EXECUTED = "EXECUTED"
        EXPIRED = "EXPIRED"

    class CancelType(Enum):
        USER = "USER"
        INSUFFICIENT_COLLATERAL = "INSUFFICIENT_COLLATERAL"
        INSUFFICIENT_MARGIN = "INSUFFICIENT_MARGIN"
        SPEED = "SPEED"
        OCO = "OCO"
        EXPIRATION = "EXPIRATION"
        PRICE_BOUND = "PRICE_BOUND"
        OUT_OF_SLIPPAGE_RANGE = "OUT_OF_SLIPPAGE_RANGE"

    Side = Side
    Symbol = Symbol
    SettleType = SettleType

    root_order_id: int
    order_id: int
    symbol: Symbol
    side: Side
    order_type: OrderType
    execution_type: ExecutionType
    settle_type: SettleType
    size: int
    price: Optional[float]
    status: Status
    expiry: date
    timestamp: datetime
    client_order_id: Optional[str] = None
    cancel_type: Optional[CancelType] = None


class OrdersResponse(ResponseBase):
    orders: list[Order]

    def __init__(self, response: dict):
        super().__init__(response)

        data = response["data"]["list"]
        self.orders = [
            Order(
                root_order_id=int(d["rootOrderId"]),
                order_id=int(d["orderId"]),
                symbol=Order.Symbol(d["symbol"]),
                side=Order.Side(d["side"]),
                order_type=Order.OrderType(d["orderType"]),
                execution_type=Order.ExecutionType(d["executionType"]),
                settle_type=Order.SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d["price"]) if d.get("price") else None,
                status=Order.Status(d["status"]),
                expiry=datetime.strptime(d["expiry"], "%Y%m%d").date(),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
                client_order_id=d.get("clientOrderId"),
                cancel_type=(
                    Order.CancelType(d["cancelType"]) if d.get("cancelType") else None
                ),
            )
            for d in data
        ]


class OrdersApi(PrivateApiBase):
    @property
    def _path(self) -> str:
        return "orders"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return OrdersResponse

    def _api_error_message(self, response: Response):
        return (
            "注文情報が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        root_order_id: list[int] = [],
        order_id: list[int] = [],
    ) -> OrdersResponse:
        query_params = []
        if root_order_id:
            query_params.append(
                f"rootOrderId={','.join([str(id) for id in root_order_id])}"
            )
        if order_id:
            query_params.append(f"orderId={','.join([str(id) for id in order_id])}")

        path_query = "&".join(query_params) if query_params else None
        return super().__call__(path_query=path_query)
