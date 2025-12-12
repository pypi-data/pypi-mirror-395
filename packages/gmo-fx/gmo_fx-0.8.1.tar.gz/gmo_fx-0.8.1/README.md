# gmo-fx-py
GMOが提供するFX用APIのSDKです。
GMOのAPIについては[こちら](https://api.coin.z.com/fxdocs/)のリファレンスを参照してください。

## インストール
```shell
pip install gmo-fx
```

## 使い方
各APIのエンドポイントの頭にgetをつけたメソッドを定義しています。
そのメソッドを実行することで、APIの呼び出しを行います。
※例：「KLine情報の取得」APIの場合
```python
from gmo_fx import KlinesApi, KlineInterval, Symbol
from datetime import datetime

response = KlinesApi()(
  symbol=Symbol.USD_JPY,
  price_type="BID",
  interval=KlineInterval.M1, # 1分足
  date=datetime.now(),
)
print(response.klines)
```
