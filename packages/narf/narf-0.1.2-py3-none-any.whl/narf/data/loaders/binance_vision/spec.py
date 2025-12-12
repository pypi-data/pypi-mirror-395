from narf.data.loaders.base_spec import NodeSpec
from narf.data.loaders.binance_vision.loader import BinanceVisionLoader


binance_vision_spec = NodeSpec("market", {
    "futures": NodeSpec("margination", {
        "um": NodeSpec("datatype", {
            "klines": NodeSpec(loader=BinanceVisionLoader),
            "trades": NodeSpec(loader=BinanceVisionLoader),
        }),
        "cm": NodeSpec("datatype", {
            "klines": NodeSpec(loader=BinanceVisionLoader),
            "trades": NodeSpec(loader=BinanceVisionLoader),
        }),
    }, loader=BinanceVisionLoader),
    "spot": NodeSpec("datatype", {
        "klines": NodeSpec(loader=BinanceVisionLoader),
        "trades": NodeSpec(loader=BinanceVisionLoader),
        "aggTrades": NodeSpec(loader=BinanceVisionLoader),
    }, loader=BinanceVisionLoader),
}, loader=BinanceVisionLoader)
