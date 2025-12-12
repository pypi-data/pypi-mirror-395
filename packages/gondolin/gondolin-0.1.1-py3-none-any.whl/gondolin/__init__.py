import sys

import yaml # Requires 'pip install PyYAML'

from .config_validator import validate_config
from .module_builder import GlobalConfig, LibConfig, ModuleBuilder
from .registry import Registry
from .safe_proxy import Policies, Rule, SafeProxy, RegistryProtocol

__version__ = "0.1.0"

__all__ = [
    "setup",
    "GlobalConfig",
    "LibConfig",
    "Policies",
    "Rule",
    "SafeProxy",
    "RegistryProtocol",
    "ModuleBuilder",
    "Registry",
]


def setup(config_path: str, registry: Registry) -> None:
    """
    Bootstrap the Gondolin environment.

    1. Reads the YAML policy file.
    2. Builds Safe Modules using the provided Registry.
    3. Injects them into sys.modules to intercept imports.
    """
    try:
        with open(config_path, "r") as f:
            raw_config: object = yaml.safe_load(f) or {"libs": {}}
    except FileNotFoundError:
        raise FileNotFoundError(f"Gondolin config not found at: {config_path}")

    config = validate_config(raw_config)

    builder = ModuleBuilder(registry)

    if "libs" in config:
        libs_dict = config["libs"]
        for lib_name, lib_conf in libs_dict.items():
            safe_mod = builder.create_safe_module(lib_name, lib_conf)
            sys.modules[lib_name] = safe_mod