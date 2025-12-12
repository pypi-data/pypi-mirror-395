import pytest
import re

from datetime import datetime
from gmo_fx.api.klines import KlinesApi, KlinesResponse
from tests.api_test_base import ApiTestBase
from typing import Callable, Literal, Optional
from unittest.mock import MagicMock, patch


class TestKlinesApi(ApiTestBase):

    def create_kline(
        self,
        open_time: str = "0000000000000",
        open: float = 0.0,
        high: float = 0.0,
        low: float = 0.0,
        close: float = 0.0,
    ) -> dict:
        return {
            "openTime": open_time,
            "open": str(open),
            "high": str(high),
            "low": str(low),
            "close": str(close),
        }

    def call_api(
        self,
        symbol: KlinesApi.Symbol,
        price_type: Literal["BID", "ASK"],
        interval: KlinesApi.KlineInterval,
        date: datetime,
    ) -> KlinesResponse:
        return KlinesApi()(
            symbol,
            price_type,
            interval,
            date,
        )

    def create_klines(
        self, size: int, kline_builder: Optional[Callable[[int], dict]] = None
    ) -> list[dict]:
        kline_builder = kline_builder or (lambda i: self.create_kline())
        return [kline_builder(i) for i in range(size)]

    @patch("gmo_fx.api.api_base.get")
    def test_klines_error(self, get_mock: MagicMock):
        self.check_404_error(
            get_mock,
            lambda: self.call_api(
                KlinesApi.Symbol.USD_JPY,
                "BID",
                KlinesApi.KlineInterval.Min1,
                datetime(2024, 1, 1),
            ),
        )

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_klines_from_response_klines_accesser(self, get_mock: MagicMock):
        expect_klines = [
            {
                "openTime": datetime(i + 1980, 1, 1),
                "open": float(i),
                "high": float(i),
                "low": float(i),
                "close": float(i),
            }
            for i in range(100)
        ]
        get_mock.return_value = self.create_response(
            data=self.create_klines(
                100,
                lambda i: self.create_kline(
                    open_time=str(int(expect_klines[i]["openTime"].timestamp()) * 1000),
                    open=expect_klines[i]["open"],
                    high=expect_klines[i]["high"],
                    low=expect_klines[i]["low"],
                    close=expect_klines[i]["close"],
                ),
            )
        )
        klines_response = self.call_api(
            KlinesApi.Symbol.USD_JPY,
            "BID",
            KlinesApi.KlineInterval.Min1,
            datetime(2024, 1, 1),
        )
        for i, expect in enumerate(expect_klines):
            assert klines_response.klines[i].open_time == expect["openTime"]
            assert klines_response.klines[i].open == expect["open"]
            assert klines_response.klines[i].high == expect["high"]
            assert klines_response.klines[i].low == expect["low"]
            assert klines_response.klines[i].close == expect["close"]

    def check_url_parameter(
        self,
        get_mock: MagicMock,
        symbol: KlinesApi.Symbol = KlinesApi.Symbol.USD_JPY,
        symbol_str: str = "USD_JPY",
        price_type: str = "ASK",
        price_type_str: str = "ASK",
        interval=KlinesApi.KlineInterval.Min1,
        interval_str="1min",
        date: datetime = datetime(2024, 1, 1),
        date_str: str = "20240101",
    ) -> None:

        get_mock.return_value = self.create_response(data=self.create_klines(1))
        self.call_api(symbol, price_type, interval, date)
        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"symbol={symbol_str}" in param
        assert f"priceType={price_type_str}" in param
        assert f"interval={interval_str}" in param
        assert f"date={date_str}" in param

    symbol_strs = [
        (KlinesApi.Symbol.USD_JPY, "USD_JPY"),
        (KlinesApi.Symbol.EUR_JPY, "EUR_JPY"),
        (KlinesApi.Symbol.GBP_JPY, "GBP_JPY"),
        (KlinesApi.Symbol.AUD_JPY, "AUD_JPY"),
        (KlinesApi.Symbol.NZD_JPY, "NZD_JPY"),
        (KlinesApi.Symbol.CAD_JPY, "CAD_JPY"),
        (KlinesApi.Symbol.CHF_JPY, "CHF_JPY"),
        (KlinesApi.Symbol.TRY_JPY, "TRY_JPY"),
        (KlinesApi.Symbol.ZAR_JPY, "ZAR_JPY"),
        (KlinesApi.Symbol.MXN_JPY, "MXN_JPY"),
        (KlinesApi.Symbol.EUR_USD, "EUR_USD"),
        (KlinesApi.Symbol.GBP_USD, "GBP_USD"),
        (KlinesApi.Symbol.AUD_USD, "AUD_USD"),
        (KlinesApi.Symbol.NZD_USD, "NZD_USD"),
    ]

    @pytest.mark.parametrize("symbol, symbol_str", symbol_strs)
    @patch("gmo_fx.api.api_base.get")
    def test_should_call_get_with_symbol(
        self, get_mock: MagicMock, symbol: KlinesApi.Symbol, symbol_str: str
    ):
        self.check_url_parameter(
            get_mock,
            symbol=symbol,
            symbol_str=symbol_str,
        )

    price_type_strs = [
        ("BID", "BID"),
        ("ASK", "ASK"),
    ]

    @pytest.mark.parametrize("price_type, price_type_str", price_type_strs)
    @patch("gmo_fx.api.api_base.get")
    def test_should_call_get_with_price_type(
        self, get_mock: MagicMock, price_type: str, price_type_str: str
    ):
        self.check_url_parameter(
            get_mock,
            price_type=price_type,
            price_type_str=price_type_str,
        )

    interval_strs = [
        (KlinesApi.KlineInterval.Min1, "1min"),
        (KlinesApi.KlineInterval.Min5, "5min"),
        (KlinesApi.KlineInterval.Min10, "10min"),
        (KlinesApi.KlineInterval.Min15, "15min"),
        (KlinesApi.KlineInterval.Min30, "30min"),
        (KlinesApi.KlineInterval.H1, "1hour"),
        (KlinesApi.KlineInterval.H4, "4hour"),
        (KlinesApi.KlineInterval.H8, "8hour"),
        (KlinesApi.KlineInterval.H12, "12hour"),
        (KlinesApi.KlineInterval.D1, "1day"),
        (KlinesApi.KlineInterval.W1, "1week"),
        (KlinesApi.KlineInterval.M1, "1month"),
    ]

    date_strs = [
        # datetime, interval, string
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.Min1, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.Min5, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.Min10, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.Min15, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.Min30, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.H1, "20240101"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.H4, "2024"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.H8, "2024"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.H12, "2024"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.D1, "2024"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.W1, "2024"),
        (datetime(2024, 1, 1, 10, 23, 12), KlinesApi.KlineInterval.M1, "2024"),
    ]

    @pytest.mark.parametrize("date, interval, string", date_strs)
    @patch("gmo_fx.api.api_base.get")
    def test_should_call_get_with_date(
        self,
        get_mock: MagicMock,
        date: datetime,
        interval: KlinesApi.KlineInterval,
        string: str,
    ):
        interval_map = dict(self.interval_strs)
        self.check_url_parameter(
            get_mock,
            interval=interval,
            interval_str=interval_map[interval],
            date=date,
            date_str=string,
        )

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response(data=self.create_klines(1))
        self.call_api(
            KlinesApi.Symbol.USD_JPY, "BID", KlinesApi.KlineInterval.D1, datetime.now()
        )
        url_match = re.search("(.*)\?.*", get_mock.mock_calls[0].args[0])
        url = url_match.group(1)
        assert url == "https://forex-api.coin.z.com/public/v1/klines"
