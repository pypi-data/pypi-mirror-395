import json
import re
from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Callable, Optional, Union
from unittest.mock import MagicMock, patch
from api.order import (
    Order,
    OrderApi,
    OrderResponse,
)


class TestOrderApi(ApiTestBase):

    def call_api(
        self,
        symbol: OrderApi.Symbol = OrderApi.Symbol.USD_JPY,
        side: OrderApi.Side = OrderApi.Side.BUY,
        size: int = 1000,
        client_order_id: Optional[str] = None,
        execution_type: OrderApi.ExecutionType = OrderApi.ExecutionType.LIMIT,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
    ) -> OrderResponse:
        return OrderApi(
            api_key="",
            secret_key="",
        )(
            symbol=symbol,
            side=side,
            size=size,
            client_order_id=client_order_id,
            execution_type=execution_type,
            limit_price=limit_price,
            stop_price=stop_price,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = [self.create_order_data()]

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "NORMAL",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 100,
        price: Optional[float] = 130.5,
        status: str = "WAITING",
        cancel_type: Optional[str] = "PRICE_BOUND",
        expiry: Optional[str] = "20220113",
        timestamp: str = "2019-03-19T02:15:06.059Z",
    ) -> dict:
        data = {
            "rootOrderId": root_order_id,
            "orderId": order_id,
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "executionType": execution_type,
            "settleType": settle_type,
            "size": str(size),
            "status": status,
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if price is not None:
            data["price"] = str(price)

        if cancel_type is not None:
            data["cancelType"] = cancel_type

        if expiry is not None:
            data["expiry"] = expiry

        return data

    @patch("gmo_fx.api.api_base.post")
    def test_404_error(self, post_mock: MagicMock):
        self.check_404_error(post_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        self.call_api()
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/order")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> OrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.orders) == 1
        return response

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert response.orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert response.orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id=None)
        assert response.orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_id=156789)
        assert response.orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in Order.Symbol:
            response = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert response.orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in Order.Side:
            response = self.check_parse_a_data(post_mock, side=side.value)
            assert response.orders[0].side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        for order_type in Order.OrderType:
            response = self.check_parse_a_data(post_mock, order_type=order_type.value)
            assert response.orders[0].order_type == order_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        for execution_type in Order.ExecutionType:
            response = self.check_parse_a_data(
                post_mock, execution_type=execution_type.value
            )
            assert response.orders[0].execution_type == execution_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in Order.SettleType:
            response = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert response.orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, size=6100)
        assert response.orders[0].size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_price(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, price=155.44)
        assert response.orders[0].price == 155.44

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_price(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, price=None)
        assert response.orders[0].price is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in Order.Status:
            response = self.check_parse_a_data(post_mock, status=status.value)
            assert response.orders[0].status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_cancel_type(self, post_mock: MagicMock):
        for cancel_type in Order.CancelType:
            response = self.check_parse_a_data(post_mock, cancel_type=cancel_type.value)
            assert response.orders[0].cancel_type == cancel_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_cancel_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, cancel_type=None)
        assert response.orders[0].cancel_type is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_expiry(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, expiry="20190418")
        assert response.orders[0].expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_expiry(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, expiry=None)
        assert response.orders[0].expiry is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        response = self.check_parse_a_data(
            post_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock) -> OrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(), self.create_order_data()]
        )
        response = self.call_api()
        assert len(response.orders) == 2

    def check_call_with(self, post_mock, **kwargs):
        post_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        kall = post_mock.call_args
        request_body = kall.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_symbol(
        self,
        post_mock: MagicMock,
    ) -> None:
        for symbol in OrderApi.Symbol:
            body = self.check_call_with(post_mock, symbol=symbol)
            assert body["symbol"] == symbol.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_side(
        self,
        post_mock: MagicMock,
    ) -> None:
        for side in OrderApi.Side:
            body = self.check_call_with(post_mock, side=side)
            assert body["side"] == side.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_size(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, size=6530)
        assert body["size"] == "6530"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_client_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, client_order_id="alfsdj32432enl")
        assert body["clientOrderId"] == "alfsdj32432enl"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_client_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, client_order_id=None)
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_execution_type(
        self,
        post_mock: MagicMock,
    ) -> None:
        for execution_type in OrderApi.ExecutionType:
            body = self.check_call_with(post_mock, execution_type=execution_type)
            assert body["executionType"] == execution_type.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_limit_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, limit_price=155.66)
        assert body["limitPrice"] == "155.66"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_limit_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, limit_price=None)
        assert "limitPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_stop_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, stop_price=154.67)
        assert body["stopPrice"] == "154.67"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_stop_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, stop_price=None)
        assert "stopPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_lower_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, lower_bound=101.93)
        assert body["lowerBound"] == "101.93"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_lower_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, lower_bound=None)
        assert "lowerBound" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_upper_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, upper_bound=99.85)
        assert body["upperBound"] == "99.85"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_upper_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, upper_bound=None)
        assert "upperBound" not in body.keys()
