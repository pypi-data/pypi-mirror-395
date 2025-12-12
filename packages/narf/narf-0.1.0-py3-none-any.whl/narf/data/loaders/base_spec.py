from dataclasses import dataclass
from typing import Optional

@dataclass
class NodeSpec:
    key: str = ""
    children: Optional[dict[str, "NodeSpec"]] = None
    loader: Optional[type] = None


class Namespace:
    def __init__(self, **children):
        for name, val in children.items():
            setattr(self, name, val)


def build(spec: NodeSpec, path: tuple[str, ...] = ()) -> object:
    # Case A: namespace
    if spec.children:
        # build children
        attrs = {
            name: build(sub, path + (name,))
            for name, sub in spec.children.items()
        }

        # create namespace object
        ns = Namespace()
        for k, v in attrs.items():
            setattr(ns, k, v)

        # also attach loader behavior
        if spec.loader:
            loader = spec.loader(path)
            # copy loader methods/attrs into namespace
            ns.load = loader.load
            ns.__loader__ = loader  # optional: keep reference to real loader

        return ns

    # Case B: pure leaf
    if spec.loader:
        return spec.loader(path)

    raise ValueError("NodeSpec must have children or leaf")
