from typing import Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.position_summary import (
    Position,
    PositionSummaryApi,
    PositionSummaryResponse,
)

from tests.api_test_base import ApiTestBase


class TestPositionSummaryApi(ApiTestBase):

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
        symbol: PositionSummaryApi.Symbol = PositionSummaryApi.Symbol.USD_JPY,
    ) -> PositionSummaryResponse:
        return PositionSummaryApi(
            api_key="",
            secret_key="",
        )(symbol=symbol)

    def create_position_summary_data(
        self,
        average_position_rate: float = 0.0,
        position_loss_gain: float = 0.0,
        side: str = "BUY",
        sum_ordered_size: int = 0,
        sum_position_size: int = 0,
        sum_total_swap: float = 0.0,
        symbol: str = "USD_JPY",
    ) -> dict:
        return {
            "averagePositionRate": str(average_position_rate),
            "positionLossGain": str(position_loss_gain),
            "side": side,
            "sumOrderedSize": str(sum_ordered_size),
            "sumPositionSize": str(sum_position_size),
            "sumTotalSwap": str(sum_total_swap),
            "symbol": symbol,
        }

    def check_parse_a_data(self, get_mock: MagicMock, **kwargs) -> Position:
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.positions) == 1
        return response.positions[0]

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_average_position_rate(self, get_mock: MagicMock):
        position = self.check_parse_a_data(get_mock=get_mock, average_position_rate=1.1)
        assert position.average_position_rate == 1.1

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_loss_gain(self, get_mock: MagicMock):
        position = self.check_parse_a_data(get_mock=get_mock, position_loss_gain=23.54)
        assert position.position_loss_gain == 23.54

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_side(self, get_mock: MagicMock):
        for side in Position.Side:

            position = self.check_parse_a_data(get_mock=get_mock, side=side.value)
            assert position.side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_ordered_size(self, get_mock: MagicMock):
        position = self.check_parse_a_data(get_mock=get_mock, sum_ordered_size=984)
        assert position.sum_ordered_size == 984

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_position_size(self, get_mock: MagicMock):
        position = self.check_parse_a_data(get_mock=get_mock, sum_position_size=1984)
        assert position.sum_position_size == 1984

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_total_swap(self, get_mock: MagicMock):
        position = self.check_parse_a_data(get_mock=get_mock, sum_total_swap=654.6)
        assert position.sum_total_swap == 654.6

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_symbol(self, get_mock: MagicMock):
        for symbol in Position.Symbol:
            position = self.check_parse_a_data(get_mock=get_mock, symbol=symbol.value)
            assert position.symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_some_positions(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[
                self.create_position_summary_data(symbol="USD_JPY"),
                self.create_position_summary_data(symbol="GBP_USD"),
            ]
        )
        response = self.call_api()
        symbols = [position.symbol for position in response.positions]
        assert symbols[0] == Position.Symbol.USD_JPY
        assert symbols[1] == Position.Symbol.GBP_USD

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=[])
        self.call_api()
        url = get_mock.mock_calls[0].args[0]
        assert (
            url
            == "https://forex-api.coin.z.com/private/v1/positionSummary?symbol=USD_JPY"
        )

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_symbol(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=[])
        self.call_api(symbol=PositionSummaryApi.Symbol.AUD_JPY)
        url = get_mock.mock_calls[0].args[0]
        assert "symbol=AUD_JPY" in url
