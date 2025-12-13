from injecty import InjectyContext
from tests.test_injecty_context import Foo, Bar, Zap, Bang

priority: int = 100


def configure(context: InjectyContext):
    context.register_impls(Foo, [Bar, Zap, Bang])
