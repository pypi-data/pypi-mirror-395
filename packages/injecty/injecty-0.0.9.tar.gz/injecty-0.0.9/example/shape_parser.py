from typing import Dict

from injecty import get_impls

from example.models.shape_abc import ShapeABC


def parse_shape(shape_dict: Dict) -> ShapeABC:
    shape_type = shape_dict.pop("type")
    impls = get_impls(ShapeABC)
    for impl in impls:
        if impl.__name__ == shape_type:
            return impl(**shape_dict)
    raise ValueError(f"no_implementation_for:{shape_type}")
