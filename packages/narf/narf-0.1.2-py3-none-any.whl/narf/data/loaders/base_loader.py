import abc
from datetime import datetime
from typing import Optional

import pandas as pd
from narf.data.loaders.base_spec import NodeSpec

class Loader(abc.ABC):
    BASE_URL: str
    URL_PATTERNS: list[tuple[tuple[str, ...], str]]

    def __init__(self, path: tuple[str, ...]):
        self.__path = path

    def get_parsed_path(self):
        from narf.data.loaders.binance_vision.spec import binance_vision_spec
        return extract_semantic_path(binance_vision_spec, self.__path)

    def _build_url(self, **kwargs):
        from narf.data.loaders.binance_vision.spec import binance_vision_spec
        template, semantic = select_pattern(self.URL_PATTERNS, self.__path, binance_vision_spec)

        ctx = {
            "base": self.BASE_URL,
            **kwargs,
            **semantic,
        }

        return template.format(**ctx)

    @abc.abstractmethod
    def load(self, date: str, start: datetime, end: Optional[datetime] = None, interval: str = "1m") -> pd.DataFrame:
        pass


def extract_semantic_path(spec: NodeSpec, path: tuple[str, ...]):
    """
    Returns a dict mapping semantic key -> actual fragment.
    Example:
        ("futures","um","klines") →
        {"market":"futures","margination":"um","datatype":"klines"}
    """
    mapping = {}
    node = spec
    i = 0

    while i < len(path):
        fragment = path[i]
        if not node.children or fragment not in node.children:
            raise ValueError("Invalid path fragment: " + fragment)

        child = node.children[fragment]

        # assign semantic key
        mapping[node.key] = fragment

        node = child
        i += 1

    return mapping


def match_pattern(pattern, path, semantic_keys):
    """
    pattern: ("futures","<margination>","<datatype>")
    path: ("futures","um","klines")
    semantic_keys: ["market","margination","datatype"]
    """

    if len(pattern) != len(path):
        return False

    for element, frag, key in zip(pattern, path, semantic_keys):

        if element.startswith("<") and element.endswith(">"):
            # semantic placeholder — must match the same semantic key
            expected_key = element[1:-1]
            if expected_key != key:
                return False

        else:
            # literal element — must match fragment exactly
            if element != frag:
                return False
            
    return True


def select_pattern(patterns: list[tuple[tuple[str, ...], str]], path: tuple[str, ...], spec: NodeSpec) -> tuple[str, dict[str, str]]:
    semantic = extract_semantic_path(spec, path)
    semantic_keys = list(semantic.keys())  # ["market","margination","datatype"]

    for pattern, template in patterns:
        if match_pattern(pattern, path, semantic_keys):
            return template, semantic

    raise ValueError(f"No pattern matches path: {path}")