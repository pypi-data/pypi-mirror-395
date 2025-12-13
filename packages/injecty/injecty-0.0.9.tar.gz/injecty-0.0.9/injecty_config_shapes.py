from example.models.circle import Circle
from example.models.shape_abc import ShapeABC
from example.models.square import Square
from injecty import InjectyContext

priority: int = 100


def configure(context: InjectyContext):
    context.register_impls(ShapeABC, [Circle, Square])
