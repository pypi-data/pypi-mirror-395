import importlib
import types
from typing import TypedDict, cast

from .safe_proxy import Policies, RegistryProtocol, SafeProxy


class PolicyConfig(TypedDict):
    target_class: str


class LibConfig(PolicyConfig):
    policies: Policies


class GlobalConfig(TypedDict):
    libs: dict[str, LibConfig]


class ModuleBuilder:
    registry: RegistryProtocol

    def __init__(self, registry: RegistryProtocol):
        self.registry = registry

    def create_safe_module(self, lib_name: str, config: LibConfig) -> types.ModuleType:
        real_lib = importlib.import_module(lib_name)
        policies_value = config["policies"]

        safe_mod = types.ModuleType(lib_name)
        cls_name = config["target_class"]
        RealClass: type[object] = cast(type[object], getattr(real_lib, cls_name))

        def factory_wrapper(*args: object, **kwargs: object) -> SafeProxy:
            instance: object = RealClass(*args, **kwargs)
            return SafeProxy(instance, policies_value, self.registry)

        setattr(safe_mod, cls_name, factory_wrapper)
        return safe_mod
