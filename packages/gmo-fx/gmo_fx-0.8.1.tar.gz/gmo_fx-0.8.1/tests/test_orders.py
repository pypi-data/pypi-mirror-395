from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.orders import (
    Order,
    OrdersApi,
    OrdersResponse,
)


class TestOrdersApi(ApiTestBase):

    def call_api(
        self,
        root_order_id: Optional[list[int]] = None,
        order_id: Optional[list[int]] = None,
    ) -> OrdersResponse:
        return OrdersApi(
            api_key="",
            secret_key="",
        )(
            root_order_id=root_order_id,
            order_id=order_id,
        )

    def create_response(
        self,
        data: Optional[dict] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = {"list": [self.create_order_data()]}

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
        size: int = 10000,
        price: Optional[float] = 135.5,
        status: str = "ORDERED",
        expiry: str = "20190418",
        timestamp: str = "2019-03-19T01:07:24.217Z",
        cancel_type: Optional[str] = None,
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

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api()
        url: str = get_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/orders")

    def check_parse_a_data(self, get_mock: MagicMock, **kwargs) -> OrdersResponse:
        get_mock.return_value = self.create_response(
            data={"list": [self.create_order_data(**kwargs)]}
        )
        response = self.call_api()
        assert len(response.orders) == 1
        return response

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_root_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, root_order_id=2536464541)
        assert response.orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id="abbb324dff")
        assert response.orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_none_without_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id=None)
        assert response.orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, order_id=156789)
        assert response.orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        for symbol in Order.Symbol:
            response = self.check_parse_a_data(get_mock, symbol=symbol.value)
            assert response.orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        for side in Order.Side:
            response = self.check_parse_a_data(get_mock, side=side.value)
            assert response.orders[0].side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_type(self, get_mock: MagicMock):
        for order_type in Order.OrderType:
            response = self.check_parse_a_data(get_mock, order_type=order_type.value)
            assert response.orders[0].order_type == order_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_execution_type(self, get_mock: MagicMock):
        for execution_type in Order.ExecutionType:
            response = self.check_parse_a_data(
                get_mock, execution_type=execution_type.value
            )
            assert response.orders[0].execution_type == execution_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type(self, get_mock: MagicMock):
        for settle_type in Order.SettleType:
            response = self.check_parse_a_data(get_mock, settle_type=settle_type.value)
            assert response.orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, size=6100)
        assert response.orders[0].size == 6100

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, price=155.44)
        assert response.orders[0].price == 155.44

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_none_without_price(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, price=None)
        assert response.orders[0].price is None

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_status(self, get_mock: MagicMock):
        for status in Order.Status:
            response = self.check_parse_a_data(get_mock, status=status.value)
            assert response.orders[0].status == status

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_cancel_type(self, get_mock: MagicMock):
        for cancel_type in Order.CancelType:
            response = self.check_parse_a_data(get_mock, cancel_type=cancel_type.value)
            assert response.orders[0].cancel_type == cancel_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_none_without_cancel_type(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, cancel_type=None)
        assert response.orders[0].cancel_type is None

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_expiry(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, expiry="20190418")
        assert response.orders[0].expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        response = self.check_parse_a_data(
            get_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_multiple_data(self, get_mock: MagicMock) -> OrdersResponse:
        get_mock.return_value = self.create_response(
            data={"list": [self.create_order_data(), self.create_order_data()]}
        )
        response = self.call_api()
        assert len(response.orders) == 2

    def check_call_with(self, get_mock, **kwargs):
        get_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        kall = get_mock.call_args
        url = kall.args[0] if kall.args else ""
        # Extract query parameters from URL
        if "?" in url:
            query_string = url.split("?", 1)[1]
            params = {}
            for param in query_string.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    params[key] = value
            return params
        return {}

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_single_root_order_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, root_order_id=[123456789])
        assert params["rootOrderId"] == "123456789"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_multiple_root_order_ids(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, root_order_id=[123456789, 987654321])
        assert params["rootOrderId"] == "123456789,987654321"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_empty_root_order_id_list(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, root_order_id=[])
        assert "rootOrderId" not in params

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_single_order_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, order_id=[123456789])
        assert params["orderId"] == "123456789"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_multiple_order_ids(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, order_id=[123456789, 223456789])
        assert params["orderId"] == "123456789,223456789"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_empty_order_id_list(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, order_id=[])
        assert "orderId" not in params

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_both_parameters(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(
            get_mock, root_order_id=[123456789], order_id=[987654321, 555666777]
        )
        assert params["rootOrderId"] == "123456789"
        assert params["orderId"] == "987654321,555666777"

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_empty_list(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"list": []})
        response = self.call_api()
        assert len(response.orders) == 0
