from typing import Type, Optional, Callable, Any, List, Dict

from injecty.injecty_context import InjectyContext, create_injecty_context, T

_DEFAULT_CONTEXT = None


def get_default_injecty_context():
    # pylint: disable=W0603
    global _DEFAULT_CONTEXT
    if _DEFAULT_CONTEXT is None:
        _DEFAULT_CONTEXT = create_injecty_context()
    return _DEFAULT_CONTEXT


def get_impls(
    base: Type[T],
    sort_key: Optional[Callable[[Type[T]], Any]] = None,
    reverse: bool = False,
    permit_no_impl: bool = False,
) -> List[Type]:
    context = get_default_injecty_context()
    impls = context.get_impls(base, sort_key, reverse, permit_no_impl)
    return impls


def get_instances(
    base: Type[T],
    sort_key: Optional[Callable[[Type[T]], Any]] = None,
    reverse: bool = False,
    kwargs: Optional[Dict] = None,
    permit_no_impl: bool = False,
) -> List[T]:
    context = get_default_injecty_context()
    instances = context.get_instances(base, sort_key, reverse, kwargs, permit_no_impl)
    return instances


def get_default_impl(
    base: Type[T],
    sort_key: Optional[Callable[[Type[T]], Any]] = None,
    reverse: bool = False,
    permit_no_impl: bool = False,
) -> Type:
    context = get_default_injecty_context()
    impl_ = context.get_default_impl(base, sort_key, reverse, permit_no_impl)
    return impl_


def get_new_default_instance(
    base: Type[T],
    sort_key: Optional[Callable[[Type[T]], Any]] = None,
    reverse: bool = False,
    kwargs: Optional[Dict] = None,
    permit_no_impl: bool = False,
) -> T:
    context = get_default_injecty_context()
    instance = context.get_new_default_instance(
        base, sort_key, reverse, kwargs, permit_no_impl
    )
    return instance
