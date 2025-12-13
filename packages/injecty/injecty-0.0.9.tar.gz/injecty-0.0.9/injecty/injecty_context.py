import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import (
    Dict,
    Type,
    Set,
    List,
    Callable,
    Optional,
    Any,
    TypeVar,
    get_type_hints,
)

_CONFIG_MODULE_PREFIX = "injecty_config"
T = TypeVar("T")


@dataclass
class InjectyContext:
    impls: Dict[Type[T], Set[Type[T]]] = field(default_factory=dict)

    def register_impl(
        self, base: Type[T], impl: Type[T], check_type: bool = True
    ) -> bool:
        if check_type and not issubclass(impl, base):
            raise TypeError(impl)
        impls = self.impls.get(base)
        if not impls:
            impls = self.impls[base] = set()
        if impl in impls:
            return False
        impls.add(impl)
        return True

    def register_impls(
        self, base: Type[T], impls: List[Type[T]], check_type: bool = True
    ) -> bool:
        result = True
        for impl in impls:
            result &= self.register_impl(base, impl, check_type)
        return result

    def deregister_impl(self, base: Type[T], impl: Type[T]) -> bool:
        impls = self.impls.get(base)
        if impls:
            if impl in impls:
                impls.remove(impl)
                return True
        return False

    def get_impls(
        self,
        base: Type[T],
        sort_key: Optional[Callable[[Type[T]], Any]] = None,
        reverse: bool = False,
        permit_no_impl: bool = False,
    ) -> List[Type]:
        impls = self.impls.get(base)
        if not impls:
            if permit_no_impl:
                return []
            raise ValueError(f"no_implementation_for:{base}")
        result = list(impls)
        if sort_key is None:
            priority = get_type_hints(base).get("priority", None)
            priority = getattr(priority, "__name__", priority)
            if priority == "int":
                sort_key = _priority_sort_key
                reverse = True
        if sort_key:
            # noinspection PyTypeChecker
            result.sort(key=sort_key, reverse=reverse)
        return result

    def get_default_impl(
        self,
        base: Type[T],
        sort_key: Optional[Callable[[Type[T]], Any]] = None,
        reverse: bool = False,
        permit_no_impl: bool = False,
    ) -> Type:
        impls = self.get_impls(base, sort_key, reverse, permit_no_impl)
        if impls:
            return impls[0]

    # pylint: disable=R0913,R0917
    def get_instances(
        self,
        base: Type[T],
        sort_key: Optional[Callable[[Type[T]], Any]] = None,
        reverse: bool = False,
        kwargs: Optional[Dict] = None,
        permit_no_impl: bool = False,
    ) -> List[T]:
        if kwargs is None:
            kwargs = {}
        impls = self.get_impls(base, sort_key, reverse, permit_no_impl)
        result = [impl(**kwargs) for impl in impls]
        return result

    # pylint: disable=R0913,R0917
    def get_new_default_instance(
        self,
        base: Type[T],
        sort_key: Optional[Callable[[Type[T]], Any]] = None,
        reverse: bool = False,
        kwargs: Optional[Dict] = None,
        permit_no_impl: bool = False,
    ) -> T:
        if kwargs is None:
            kwargs = {}
        impls = self.get_impls(base, sort_key, reverse, permit_no_impl)
        if impls:
            result = impls[0](**kwargs)
            return result


def create_injecty_context(config_module_prefix: str = _CONFIG_MODULE_PREFIX):
    context = InjectyContext()
    module_info = (
        m for m in pkgutil.iter_modules() if m.name.startswith(config_module_prefix)
    )
    modules = [importlib.import_module(m.name) for m in module_info]
    modules.sort(key=lambda m: m.priority, reverse=False)
    for m in modules:
        getattr(m, "configure")(context)
    return context


def _priority_sort_key(n):
    return n.priority
