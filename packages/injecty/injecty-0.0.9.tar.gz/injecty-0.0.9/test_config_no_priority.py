from injecty import InjectyContext
from tests.test_injecty_context import Foo, Bar, Zap, Bang


def configure(context: InjectyContext):
    context.register_impls(Foo, [Bar, Zap, Bang])
