from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.symbols import Rule, SymbolsApi, SymbolsResponse

from tests.api_test_base import ApiTestBase


class TestSymbolsApi(ApiTestBase):
    SYMBOLS = [
        "USD_JPY",
        "EUR_JPY",
        "GBP_JPY",
        "AUD_JPY",
        "NZD_JPY",
        "CAD_JPY",
        "CHF_JPY",
        "TRY_JPY",
        "ZAR_JPY",
        "MXN_JPY",
        "EUR_USD",
        "GBP_USD",
        "AUD_USD",
        "NZD_USD",
    ]

    SYMBOLS_TABLE = {
        Rule.Symbol.USD_JPY: "USD_JPY",
        Rule.Symbol.EUR_JPY: "EUR_JPY",
        Rule.Symbol.GBP_JPY: "GBP_JPY",
        Rule.Symbol.AUD_JPY: "AUD_JPY",
        Rule.Symbol.NZD_JPY: "NZD_JPY",
        Rule.Symbol.CAD_JPY: "CAD_JPY",
        Rule.Symbol.CHF_JPY: "CHF_JPY",
        Rule.Symbol.TRY_JPY: "TRY_JPY",
        Rule.Symbol.ZAR_JPY: "ZAR_JPY",
        Rule.Symbol.MXN_JPY: "MXN_JPY",
        Rule.Symbol.EUR_USD: "EUR_USD",
        Rule.Symbol.GBP_USD: "GBP_USD",
        Rule.Symbol.AUD_USD: "AUD_USD",
        Rule.Symbol.NZD_USD: "NZD_USD",
    }

    def call_api(
        self,
    ) -> SymbolsResponse:
        return SymbolsApi()()

    def create_symbol_data(
        self,
        symbol: str = "USD_JPY",
        min_open_order_size: int = 0,
        max_order_size: int = 0,
        size_step: int = 0,
        tick_size: float = 0.0,
    ) -> dict:
        return {
            "symbol": symbol,
            "minOpenOrderSize": str(min_open_order_size),
            "maxOrderSize": str(max_order_size),
            "sizeStep": str(size_step),
            "tickSize": str(tick_size),
        }

    def create_symbols_data(
        self, symbols_data_builder: Optional[Callable[[str], dict]] = None
    ) -> list[dict]:
        symbols_data_builder = symbols_data_builder or (
            lambda symbol: self.create_symbol_data(symbol=symbol)
        )
        return [symbols_data_builder(symbol) for symbol in self.SYMBOLS]

    @patch("gmo_fx.api.api_base.get")
    def test_symbols_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbols_from_symbols(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data=self.create_symbols_data())
        symbols_response = self.call_api()
        symbols = [rule.symbol for rule in symbols_response.rules]
        for symbol in Rule.Symbol:
            assert symbol in symbols
            symbols.remove(symbol)
        else:
            assert len(symbols) == 0

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_min_open_order_size_from_symbols(self, get_mock: MagicMock):
        def fixture_min_open_order_size(symbol: str):
            return self.SYMBOLS.index(symbol) * 100

        def fixture_symbols_data(symbol: str) -> dict:
            size = fixture_min_open_order_size(symbol)
            return self.create_symbol_data(symbol, min_open_order_size=size)

        get_mock.return_value = self.create_response(
            data=self.create_symbols_data(symbols_data_builder=fixture_symbols_data)
        )
        rules = self.call_api().rules
        for rule in rules:
            assert rule.min_open_order_size == fixture_min_open_order_size(
                self.SYMBOLS_TABLE[rule.symbol]
            )

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_max_order_size_from_symbols(self, get_mock: MagicMock):
        def fixture_max_order_size(symbol: str):
            return self.SYMBOLS.index(symbol) * 100

        def fixture_symbols_data(symbol: str) -> dict:
            size = fixture_max_order_size(symbol)
            return self.create_symbol_data(symbol, max_order_size=size)

        get_mock.return_value = self.create_response(
            data=self.create_symbols_data(symbols_data_builder=fixture_symbols_data)
        )
        rules = self.call_api().rules
        for rule in rules:
            assert rule.max_order_size == fixture_max_order_size(
                self.SYMBOLS_TABLE[rule.symbol]
            )

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size_step_from_symbols(self, get_mock: MagicMock):
        def fixture_size_step(symbol: str):
            return self.SYMBOLS.index(symbol) * 100

        def fixture_symbols_data(symbol: str) -> dict:
            step = fixture_size_step(symbol)
            return self.create_symbol_data(symbol, size_step=step)

        get_mock.return_value = self.create_response(
            data=self.create_symbols_data(symbols_data_builder=fixture_symbols_data)
        )
        rules = self.call_api().rules
        for rule in rules:
            assert rule.size_step == fixture_size_step(self.SYMBOLS_TABLE[rule.symbol])

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_tick_size_from_symbols(self, get_mock: MagicMock):
        def fixture_tick_size(symbol: str):
            return (self.SYMBOLS.index(symbol) / 3) * 100

        def fixture_symbols_data(symbol: str) -> dict:
            size = fixture_tick_size(symbol)
            return self.create_symbol_data(symbol, tick_size=size)

        get_mock.return_value = self.create_response(
            data=self.create_symbols_data(symbols_data_builder=fixture_symbols_data)
        )
        rules = self.call_api().rules
        for rule in rules:
            assert rule.tick_size == fixture_tick_size(self.SYMBOLS_TABLE[rule.symbol])

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=self.create_symbols_data())
        self.call_api()
        url = get_mock.mock_calls[0].args[0]
        assert url == "https://forex-api.coin.z.com/public/v1/symbols"
