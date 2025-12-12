from datetime import datetime, timezone
from typing import Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.open_positions import (
    OpenPosition,
    OpenPositionsApi,
    OpenPositionsResponse,
)

from tests.api_test_base import ApiTestBase


class TestOpenPositionApi(ApiTestBase):

    def call_api(
        self,
        symbol: Optional[OpenPositionsApi.Symbol] = None,
        prev_id: Optional[int] = None,
        count: Optional[int] = None,
    ) -> OpenPositionsResponse:
        return OpenPositionsApi(
            api_key="",
            secret_key="",
        )(symbol=symbol, prev_id=prev_id, count=count)

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = [self.create_open_position_data()]

        return super().create_response(
            data={"list": data},
            status_code=status_code,
            text=text,
        )

    def create_open_position_data(
        self,
        position_id: int = 0,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        size: int = 100,
        ordered_size: int = 1,
        price: float = 100.5,
        loss_gain: float = 10.5,
        total_swap: float = 0.1,
        timestamp: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    ) -> dict:
        return {
            "positionId": position_id,
            "symbol": symbol,
            "side": side,
            "size": str(size),
            "orderedSize": str(ordered_size),
            "price": str(price),
            "lossGain": str(loss_gain),
            "totalSwap": str(total_swap),
            "timestamp": timestamp,
        }

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
        assert url.startswith("https://forex-api.coin.z.com/private/v1/openPositions")

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_symbol(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(symbol=OpenPositionsApi.Symbol.GBP_USD)
        url = get_mock.mock_calls[0].args[0]
        assert "symbol=GBP_USD" in url

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_symbol(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(symbol=None)
        url = get_mock.mock_calls[0].args[0]
        assert "symbol=" not in url

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_prev_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(prev_id=12345)
        url = get_mock.mock_calls[0].args[0]
        assert "prevId=12345" in url

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_prev_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(prev_id=None)
        url = get_mock.mock_calls[0].args[0]
        assert "prevId=" not in url

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_count(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(count=12345)
        url = get_mock.mock_calls[0].args[0]
        assert "count=12345" in url

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_count(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(count=None)
        url = get_mock.mock_calls[0].args[0]
        assert "count=" not in url

    def check_parse_a_data(
        self, get_mock: MagicMock, **kwargs
    ) -> OpenPositionsResponse:
        get_mock.return_value = self.create_response(
            data=[self.create_open_position_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.open_positions) == 1
        return response

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, position_id=123123)
        assert response.open_positions[0].position_id == 123123

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        for symbol in OpenPosition.Symbol:
            response = self.check_parse_a_data(get_mock, symbol=symbol.value)
            assert response.open_positions[0].symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        for side in OpenPosition.Side:
            response = self.check_parse_a_data(get_mock, side=side.value)
            assert response.open_positions[0].side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, size=130204)
        assert response.open_positions[0].size == 130204

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_ordersize(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, ordered_size=99864)
        assert response.open_positions[0].ordered_size == 99864

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, price=101.123)
        assert response.open_positions[0].price == 101.123

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_loss_gain(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, loss_gain=10500.66)
        assert response.open_positions[0].loss_gain == 10500.66

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_total_swap(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, total_swap=166.13)
        assert response.open_positions[0].total_swap == 166.13

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        response = self.check_parse_a_data(
            get_mock, timestamp="2019-03-21T05:18:09.011Z"
        )
        assert response.open_positions[0].timestamp == datetime(
            2019, 3, 21, 5, 18, 9, 11000, tzinfo=timezone.utc
        )
