from collections.abc import Mapping
from typing import Callable, Protocol, TypeVar, cast

T = TypeVar("T")

# Type alias for policies
Rule = str | dict[str, object]
Policies = dict[str, list[Rule]]


class RegistryProtocol(Protocol):
    def get(self, name: str) -> Callable[..., object]: ...


class SafeProxy:
    _target: object
    _policies: Policies
    _registry: RegistryProtocol
    _prefix: str

    def __init__(self, target: object, policies: Policies, registry: RegistryProtocol, prefix: str = ""):
        self._target = target
        self._policies = policies
        self._registry = registry
        self._prefix = prefix

    def _apply_decorators(self, func: Callable[..., T], rule_list: list[Rule]) -> Callable[..., T]:
        wrapped: Callable[..., T] = func

        for rule in reversed(rule_list):
            assert isinstance(rule, (str, dict)), f"Invalid rule type: {type(rule)}. Expected str or dict."

            if isinstance(rule, str):
                dec = self._registry.get(rule)
                decorator_func = cast(Callable[[Callable[..., T]], Callable[..., T]], dec)
                wrapped = decorator_func(wrapped)
            else:
                if len(rule) != 1:
                    raise ValueError(f"Invalid rule format: {rule}. Expected single key-value pair.")

                decorator_name, decorator_args = next(iter(rule.items()))
                decorator_factory = self._registry.get(decorator_name)

                if isinstance(decorator_args, Mapping):
                    decorator_args = cast(Mapping[object, object], decorator_args)
                    if not all(isinstance(k, str) for k in decorator_args.keys()):
                        raise ValueError(
                            f"Invalid kwargs for decorator '{decorator_name}': keys must be str"
                        )
                    decorator_args = cast(Mapping[str, object], decorator_args)
                    decorator_func = cast(
                        Callable[[Callable[..., T]], Callable[..., T]],
                        decorator_factory(**decorator_args),
                    )
                else:
                    decorator_func = cast(
                        Callable[[Callable[..., T]], Callable[..., T]],
                        decorator_factory(decorator_args),
                    )

                wrapped = decorator_func(wrapped)
        return wrapped

    def __getattr__(self, name: str) -> object:
        path = f"{self._prefix}.{name}" if self._prefix else name

        is_exact = path in self._policies
        is_parent = any(k.startswith(path + ".") for k in self._policies.keys())

        if not (is_exact or is_parent):
            raise PermissionError(f"Gondolin Security: Access to '{path}' is denied.")

        real_attr: object = cast(object, getattr(self._target, name))

        if is_exact:
            if callable(real_attr):
                return self._apply_decorators(real_attr, self._policies[path])
            return real_attr

        return SafeProxy(real_attr, self._policies, self._registry, path)
