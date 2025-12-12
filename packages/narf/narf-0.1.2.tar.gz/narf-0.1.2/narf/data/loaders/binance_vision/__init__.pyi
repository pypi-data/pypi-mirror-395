from narf.data.loaders.binance_vision.loader import BinanceVisionLoader as LoaderType

class BinanceVisionFuturesUmKlines(LoaderType):
    pass

class BinanceVisionFuturesUmTrades(LoaderType):
    pass

class BinanceVisionFuturesUm:
    klines: BinanceVisionFuturesUmKlines
    trades: BinanceVisionFuturesUmTrades

class BinanceVisionFuturesCmKlines(LoaderType):
    pass

class BinanceVisionFuturesCmTrades(LoaderType):
    pass

class BinanceVisionFuturesCm:
    klines: BinanceVisionFuturesCmKlines
    trades: BinanceVisionFuturesCmTrades

class BinanceVisionFutures(LoaderType):
    um: BinanceVisionFuturesUm
    cm: BinanceVisionFuturesCm

class BinanceVisionSpotKlines(LoaderType):
    pass

class BinanceVisionSpotTrades(LoaderType):
    pass

class BinanceVisionSpotAggtrades(LoaderType):
    pass

class BinanceVisionSpot(LoaderType):
    klines: BinanceVisionSpotKlines
    trades: BinanceVisionSpotTrades
    aggTrades: BinanceVisionSpotAggtrades

class BinanceVision(LoaderType):
    futures: BinanceVisionFutures
    spot: BinanceVisionSpot
binance: BinanceVision

def generate_pyi():
    pass