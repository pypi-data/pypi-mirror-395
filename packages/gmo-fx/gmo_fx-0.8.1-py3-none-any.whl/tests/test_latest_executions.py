from datetime import datetime, timedelta, timezone
import re
from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.latest_executions import (
    Execution,
    LatestExecutionsApi,
    LatestExecutionsResponse,
)

from tests.api_test_base import ApiTestBase


class TestLatestExecutionsApi(ApiTestBase):

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        return super().create_response(
            data={"list": data},
            status_code=status_code,
            text=text,
        )

    def call_api(
        self,
        symbol: LatestExecutionsApi.Symbol = LatestExecutionsApi.Symbol.USD_JPY,
        count: int = 100,
    ) -> LatestExecutionsResponse:
        return LatestExecutionsApi(
            api_key="",
            secret_key="",
        )(symbol, count)

    def create_execution_data(
        self,
        amount: float = 0.0,
        execution_id: int = 0,
        client_order_id: str = "id",
        order_id: int = 0,
        position_id: int = 0,
        symbol: str = "USD_JPY",
        side: str = "SELL",
        settle_type: str = "CLOSE",
        size: int = 1,
        price: float = 0.0,
        loss_gain: int = 0,
        fee: int = 0,
        settled_swap: float = 0.0,
        timestamp: str = "2022-11-12T13:56:12.02113Z",
    ) -> dict:
        return {
            "amount": str(amount),
            "executionId": execution_id,
            "clientOrderId": client_order_id,
            "orderId": order_id,
            "positionId": position_id,
            "symbol": symbol,
            "side": side,
            "settleType": settle_type,
            "size": str(size),
            "price": str(price),
            "lossGain": str(loss_gain),
            "fee": str(fee),
            "settledSwap": str(settled_swap),
            "timestamp": timestamp,
        }

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    def check_parse_a_data(self, get_mock: MagicMock, **kwargs) -> Execution:
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.executions) == 1
        return response.executions[0]

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_amount(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, amount=1.2)
        assert execution.amount == 1.2

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_execution_id(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, execution_id=12)
        assert execution.execution_id == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_client_order_id(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, client_order_id="fdsa")
        assert execution.client_order_id == "fdsa"

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_id(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, order_id=12)
        assert execution.order_id == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_id(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, position_id=12)
        assert execution.position_id == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        for symbol in Execution.Symbol:
            execution = self.check_parse_a_data(get_mock, symbol=symbol.value)
            assert execution.symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        for side in Execution.Side:
            execution = self.check_parse_a_data(get_mock, side=side.value)
            assert execution.side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type(self, get_mock: MagicMock):
        for settle_type in Execution.SettleType:
            execution = self.check_parse_a_data(get_mock, settle_type=settle_type.value)
            assert execution.settle_type == settle_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, size=1654)
        assert execution.size == 1654

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, price=100.5)
        assert execution.price == 100.5

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_loss_gain(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, loss_gain=30)
        assert execution.loss_gain == 30

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_fee(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, fee=40)
        assert execution.fee == 40

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settled_swap(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(get_mock, settled_swap=40.4)
        assert execution.settled_swap == 40.4

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        execution = self.check_parse_a_data(
            get_mock, timestamp="2024-01-02T20:11:00.000Z"
        )
        assert execution.timestamp == datetime(2024, 1, 2, 20, 11, tzinfo=timezone.utc)

    @patch("gmo_fx.api.api_base.get")
    def test_should_set_url_symbol(self, get_mock: MagicMock):

        get_mock.return_value = self.create_response(
            data=[self.create_execution_data()]
        )
        response = self.call_api(symbol=LatestExecutionsApi.Symbol.EUR_USD)

        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"symbol=EUR_USD" in param

    @patch("gmo_fx.api.api_base.get")
    def test_should_set_url_count(self, get_mock: MagicMock):

        get_mock.return_value = self.create_response(
            data=[self.create_execution_data()]
        )
        response = self.call_api(count=20)

        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"count=20" in param

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=[])
        self.call_api()
        url_match = re.search("(.*)\?.*", get_mock.mock_calls[0].args[0])
        url = url_match.group(1)
        assert url == "https://forex-api.coin.z.com/private/v1/latestExecutions"
