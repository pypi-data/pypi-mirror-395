import ast
import os
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class NodeSpec:
    children: Optional[Dict[str, "NodeSpec"]] = None
    loader: Optional[type] = None


def generate_pyi(
    spec: NodeSpec,
    root_class_name: str,
    root_var_name: str,
    package_name: str,
    loader_import: str,
    loader_class_name: str = "LoaderType",
):
    """
    Generates:

        narf/data/loaders/<package_name>/__init__.pyi

    The loader class name is taken from `loader_class_name`.
    """

    module = ast.Module(body=[], type_ignores=[])

    # ------------------------------------------------------------
    # Import loader dynamically under unified name LoaderType
    # ------------------------------------------------------------
    # Example:
    # from narf.data.loaders.binance_vision.loader import BinanceVisionLoader as LoaderType
    import_stmt = f"from {loader_import} import {loader_class_name} as LoaderType"
    module.body.extend(ast.parse(import_stmt).body)

    class_defs: list[ast.ClassDef] = []

    # ------------------------------------------------------------
    # Class builder
    # ------------------------------------------------------------
    def make_class(name: str, fields: Dict[str, str], bases: list[str]):
        return ast.ClassDef(
            name=name,
            bases=[ast.Name(id=b, ctx=ast.Load()) for b in bases],
            keywords=[],
            decorator_list=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id=field, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    value=None,
                    simple=1,
                )
                for field, typ in fields.items()
            ] or [ast.Pass()],
        )

    # ------------------------------------------------------------
    # DFS
    # ------------------------------------------------------------
    def visit(node: NodeSpec, name: str):
        bases = []

        # This node also behaves as a loader
        if node.loader:
            bases.append("LoaderType")

        fields: Dict[str, str] = {}

        if node.children:
            for ch_name, ch_spec in node.children.items():

                # child namespace OR non-leaf loader
                if ch_spec.children or ch_spec.loader:
                    child_class_name = name + ch_name.capitalize()
                    fields[ch_name] = child_class_name
                    visit(ch_spec, child_class_name)

                else:
                    # pure leaf loader
                    fields[ch_name] = "LoaderType"

        # Always create a class for this node
        class_defs.append(make_class(name, fields, bases))

    # Start from root class
    visit(spec, root_class_name)

    # ------------------------------------------------------------
    # Add classes
    # ------------------------------------------------------------
    module.body.extend(class_defs)

    # ------------------------------------------------------------
    # Add final variable: <root_var_name>: <root_class_name>
    # ------------------------------------------------------------
    module.body.extend([
        ast.AnnAssign(
            target=ast.Name(id=root_var_name, ctx=ast.Store()),
            annotation=ast.Name(id=root_class_name, ctx=ast.Load()),
            value=None,
            simple=1,
        ),
        # Keep your dummy function (unchanged)
        ast.FunctionDef(
            name="generate_pyi",
            args=ast.arguments(
                posonlyargs=[],
                args=[],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=[ast.Pass()],
            decorator_list=[],
            returns=None,
        )
    ])

    # ------------------------------------------------------------
    # Write file to:
    #     narf/data/loaders/<package_name>/__init__.pyi
    # ------------------------------------------------------------
    ast.fix_missing_locations(module)
    source = ast.unparse(module)

    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    out_path = os.path.join(this_dir, "loaders", package_name, "__init__.pyi")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(source)

    return out_path
