import json
import re
from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Callable, Optional, Union
from unittest.mock import MagicMock, patch
from gmo_fx.api.change_oco_order import (
    Order,
    ChangeOcoOrderApi,
    ChangeOcoOrderResponse,
)


class TestChangeOcoOrderApi(ApiTestBase):

    def call_api(
        self,
        root_order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> ChangeOcoOrderResponse:
        return ChangeOcoOrderApi(
            api_key="",
            secret_key="",
        )(
            root_order_id=root_order_id,
            client_order_id=client_order_id,
            limit_price=limit_price,
            stop_price=stop_price,
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
        order_type: str = "OCO",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 100,
        price: Optional[float] = 130.5,
        status: str = "ORDERED",
        cancel_type: Optional[str] = "OCO",
        expiry: str = "20220113",
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
            "expiry": expiry,
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if price is not None:
            data["price"] = str(price)

        if cancel_type is not None:
            data["cancelType"] = cancel_type

        return data

    @patch("gmo_fx.api.api_base.post")
    def test_404_error(self, post_mock: MagicMock):
        self.check_404_error(post_mock, lambda: self.call_api(root_order_id=123456789))

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        self.call_api(root_order_id=123456789)
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/changeOcoOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> Order:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api(root_order_id=123456789)
        assert len(response.orders) == 1
        return response.orders[0]

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert order.root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert order.client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id=None)
        assert order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, order_id=156789)
        assert order.order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in Order.Symbol:
            order = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert order.symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in Order.Side:
            order = self.check_parse_a_data(post_mock, side=side.value)
            assert order.side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        for order_type in Order.OrderType:
            order = self.check_parse_a_data(post_mock, order_type=order_type.value)
            assert order.order_type == order_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        for execution_type in Order.ExecutionType:
            order = self.check_parse_a_data(
                post_mock, execution_type=execution_type.value
            )
            assert order.execution_type == execution_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in Order.SettleType:
            order = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert order.settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, size=6100)
        assert order.size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_price(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, price=155.44)
        assert order.price == 155.44

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_price(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, price=None)
        assert order.price is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in Order.Status:
            order = self.check_parse_a_data(post_mock, status=status.value)
            assert order.status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_cancel_type(self, post_mock: MagicMock):
        for cancel_type in Order.CancelType:
            order = self.check_parse_a_data(post_mock, cancel_type=cancel_type.value)
            assert order.cancel_type == cancel_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_cancel_type(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, cancel_type=None)
        assert order.cancel_type is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_expiry(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, expiry="20190418")
        assert order.expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, timestamp="2024-09-13T15:21:03.059Z")
        assert order.timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(), self.create_order_data()]
        )
        response = self.call_api(root_order_id=123456789)
        assert len(response.orders) == 2

    def check_call_with(self, post_mock, **kwargs):
        post_mock.return_value = self.create_response()
        # Ensure at least root_order_id or client_order_id is provided
        if "root_order_id" not in kwargs and "client_order_id" not in kwargs:
            kwargs["root_order_id"] = 123456789
        self.call_api(**kwargs)
        kall = post_mock.call_args
        request_body = kall.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_root_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, root_order_id=987654321)
        assert body["rootOrderId"] == 987654321

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_root_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(
            post_mock, root_order_id=None, client_order_id="test123"
        )
        assert "rootOrderId" not in body.keys()

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
        body = self.check_call_with(
            post_mock, client_order_id=None, root_order_id=123456789
        )
        assert "clientOrderId" not in body.keys()

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
        body = self.check_call_with(post_mock, limit_price=None, stop_price=154.67)
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
        body = self.check_call_with(post_mock, stop_price=None, limit_price=155.66)
        assert "stopPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_both_prices(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, limit_price=140.525, stop_price=145.607)
        assert body["limitPrice"] == "140.525"
        assert body["stopPrice"] == "145.607"
