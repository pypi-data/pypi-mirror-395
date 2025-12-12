from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.ticker import Ticker, TickerApi, TickerResponse
from datetime import datetime

from tests.api_test_base import ApiTestBase


class TestTickerApi(ApiTestBase):
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
        Ticker.Symbol.USD_JPY: "USD_JPY",
        Ticker.Symbol.EUR_JPY: "EUR_JPY",
        Ticker.Symbol.GBP_JPY: "GBP_JPY",
        Ticker.Symbol.AUD_JPY: "AUD_JPY",
        Ticker.Symbol.NZD_JPY: "NZD_JPY",
        Ticker.Symbol.CAD_JPY: "CAD_JPY",
        Ticker.Symbol.CHF_JPY: "CHF_JPY",
        Ticker.Symbol.TRY_JPY: "TRY_JPY",
        Ticker.Symbol.ZAR_JPY: "ZAR_JPY",
        Ticker.Symbol.MXN_JPY: "MXN_JPY",
        Ticker.Symbol.EUR_USD: "EUR_USD",
        Ticker.Symbol.GBP_USD: "GBP_USD",
        Ticker.Symbol.AUD_USD: "AUD_USD",
        Ticker.Symbol.NZD_USD: "NZD_USD",
    }

    def create_ticker_data(
        self,
        symbol: str,
        status: str = "OPEN",
        ask: float = 0.0,
        bid: float = 0.0,
        timestamp: Optional[datetime] = None,
    ) -> dict:
        return {
            "symbol": symbol,
            "ask": ask,
            "bid": bid,
            "timestamp": (timestamp or datetime.now()).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "status": status,
        }

    def create_tickers_data(
        self, exchange_data_builder: Optional[Callable[[str], dict]] = None
    ) -> list[dict]:
        exchange_data_builder = exchange_data_builder or self.create_ticker_data
        return [exchange_data_builder(symbol) for symbol in self.SYMBOLS]

    def call_api(
        self,
    ) -> TickerResponse:
        return TickerApi()()

    @patch("gmo_fx.api.api_base.get")
    def test_ticker_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbols_from_ticker(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data=self.create_tickers_data())
        ticker_response = self.call_api()
        symbols = [ticker.symbol for ticker in ticker_response.tickers]
        for symbol in Ticker.Symbol:
            assert symbol in symbols
            symbols.remove(symbol)
        else:
            assert len(symbols) == 0

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_bid_ask_from_ticker(self, get_mock: MagicMock):
        def fixture_ask_bid(symbol: str):
            return self.SYMBOLS.index(symbol), self.SYMBOLS.index(symbol) * 100

        def fixture_ticker_data(symbol: str) -> dict:
            ask, bid = fixture_ask_bid(symbol)
            return self.create_ticker_data(symbol, ask=ask, bid=bid)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = self.call_api().tickers
        for rate in rates:
            assert rate.ask == fixture_ask_bid(self.SYMBOLS_TABLE[rate.symbol])[0]
            assert rate.bid == fixture_ask_bid(self.SYMBOLS_TABLE[rate.symbol])[1]

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp_from_ticker(self, get_mock: MagicMock):
        def fixture_timestamp(symbol: str):
            return datetime(2000, 12, self.SYMBOLS.index(symbol) + 1)  # 0日はないので

        def fixture_ticker_data(symbol: str) -> dict:
            timestamp = fixture_timestamp(symbol)
            return self.create_ticker_data(symbol, timestamp=timestamp)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = self.call_api().tickers
        for rate in rates:
            assert rate.timestamp == fixture_timestamp(self.SYMBOLS_TABLE[rate.symbol])

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_status_from_ticker(self, get_mock: MagicMock):
        def fixture_status(symbol: str):
            statuses = ["OPEN", "CLOSE"]
            return statuses[self.SYMBOLS.index(symbol) % len(statuses)]

        def fixture_ticker_data(symbol: str) -> dict:
            status = fixture_status(symbol)
            return self.create_ticker_data(symbol, status=status)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = self.call_api().tickers
        for rate in rates:
            status_str = fixture_status(self.SYMBOLS_TABLE[rate.symbol])
            for status in ["OPEN", "CLOSE"]:
                if status == status_str:
                    assert rate.status == status
                    break
            else:
                assert False

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=self.create_tickers_data())
        self.call_api()
        url = get_mock.mock_calls[0].args[0]
        assert url == "https://forex-api.coin.z.com/public/v1/ticker"
