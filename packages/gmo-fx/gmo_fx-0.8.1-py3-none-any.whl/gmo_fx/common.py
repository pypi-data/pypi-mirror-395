from enum import Enum


class Symbol(Enum):
    """銘柄"""

    USD_JPY = "USD_JPY"
    EUR_JPY = "EUR_JPY"
    GBP_JPY = "GBP_JPY"
    AUD_JPY = "AUD_JPY"
    NZD_JPY = "NZD_JPY"
    CAD_JPY = "CAD_JPY"
    CHF_JPY = "CHF_JPY"
    TRY_JPY = "TRY_JPY"
    ZAR_JPY = "ZAR_JPY"
    MXN_JPY = "MXN_JPY"
    EUR_USD = "EUR_USD"
    GBP_USD = "GBP_USD"
    AUD_USD = "AUD_USD"
    NZD_USD = "NZD_USD"


class Side(Enum):
    """売買区分
    BUY: 売
    SELL: 買
    """

    BUY = "BUY"
    SELL = "SELL"


class SettleType(Enum):
    """決済区分"""

    OPEN = "OPEN"
    CLOSE = "CLOSE"


class OrderType(Enum):
    """取引区分"""

    NORMAL = "NORMAL"
    OCO = "OCO"
