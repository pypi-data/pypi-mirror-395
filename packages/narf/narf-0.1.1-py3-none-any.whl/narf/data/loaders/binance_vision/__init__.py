from narf.data.loaders.base_spec import build
from .spec import binance_vision_spec


binance = build(binance_vision_spec)

 
def generate_pyi():
    from narf.data.generate import generate_pyi

    generate_pyi(
        spec=binance_vision_spec,
        root_class_name="BinanceVision",
        root_var_name="binance",
        package_name="binance_vision",
        loader_import="narf.data.loaders.binance_vision.loader",
        loader_class_name="BinanceVisionLoader",
    )


__all__ = ["binance", "generate_pyi"]
