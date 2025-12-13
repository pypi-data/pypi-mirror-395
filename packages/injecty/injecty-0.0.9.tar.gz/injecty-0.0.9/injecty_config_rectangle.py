from example.models.rectangle import Rectangle
from example.models.shape_abc import ShapeABC
from injecty import InjectyContext

priority: int = 100


def configure(context: InjectyContext):
    context.register_impl(ShapeABC, Rectangle)
