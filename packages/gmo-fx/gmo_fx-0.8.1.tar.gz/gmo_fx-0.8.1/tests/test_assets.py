import re

from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.common import Symbol
from gmo_fx.api.assets import AssetsApi, AssetsResponse

from tests.api_test_base import ApiTestBase


class TestAssetsApi(ApiTestBase):

    def call_api(
        self,
    ) -> AssetsResponse:
        return AssetsApi(
            api_key="",
            secret_key="",
        )()

    def create_assets_data(
        self,
        equity: int = 0,
        available_amount: int = 0,
        balance: int = 0,
        estimated_trade_fee: float = 0.0,
        margin: int = 0,
        margin_ratio: float = 0.0,
        position_loss_gain: float = 0.0,
        total_swap: float = 0.0,
        transferable_amount: int = 0,
    ) -> dict:
        return [
            {
                "equity": equity,
                "availableAmount": available_amount,
                "balance": balance,
                "estimatedTradeFee": estimated_trade_fee,
                "margin": margin,
                "marginRatio": margin_ratio,
                "positionLossGain": position_loss_gain,
                "totalSwap": total_swap,
                "transferableAmount": transferable_amount,
            }
        ]

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_equity(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(equity=1)
        )
        response = self.call_api()
        equities = [asset.equity for asset in response.assets]
        assert equities[0] == 1

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_available_amount(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(available_amount=1)
        )
        response = self.call_api()
        available_amounts = [asset.available_amount for asset in response.assets]
        assert available_amounts[0] == 1

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_balance(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(balance=1)
        )
        response = self.call_api()
        balances = [asset.balance for asset in response.assets]
        assert balances[0] == 1

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_estimated_trade_fee(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(estimated_trade_fee=1.2)
        )
        response = self.call_api()
        estimated_trade_fees = [asset.estimated_trade_fee for asset in response.assets]
        assert estimated_trade_fees[0] == 1.2

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_margin(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(margin=1)
        )
        response = self.call_api()
        margins = [asset.margin for asset in response.assets]
        assert margins[0] == 1

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_margin_ratio(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(margin_ratio=1.4)
        )
        response = self.call_api()
        margin_ratios = [asset.margin_ratio for asset in response.assets]
        assert margin_ratios[0] == 1.4

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_loss_gain(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(position_loss_gain=1.4)
        )
        response = self.call_api()
        position_loss_gains = [asset.position_loss_gain for asset in response.assets]
        assert position_loss_gains[0] == 1.4

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_total_swap(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(total_swap=1.4)
        )
        response = self.call_api()
        total_swaps = [asset.total_swap for asset in response.assets]
        assert total_swaps[0] == 1.4

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_transferable_amount(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(transferable_amount=1)
        )
        response = self.call_api()
        transferable_amounts = [asset.transferable_amount for asset in response.assets]
        assert transferable_amounts[0] == 1

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(equity=1)
        )
        self.call_api()
        url = get_mock.mock_calls[0].args[0]
        assert url == "https://forex-api.coin.z.com/private/v1/account/assets"
