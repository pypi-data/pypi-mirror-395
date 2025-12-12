import sys
import yaml
import importlib
from .core import ModuleBuilder
from .registry import Registry

__version__ = "0.1.0"

def setup(policies_path: str, registry: Registry):
    """
    Bootstrap the Gondolin environment.
    Reads the YAML policy and injects Safe Proxies into sys.modules.
    """
    with open(policies_path, "r") as f:
        policies = yaml.safe_load(f)

    builder = ModuleBuilder(registry)

    if "libs" in policies:
        for lib_name, lib_conf in policies["libs"].items():
            # Build the safe version
            safe_mod = builder.create_safe_module(lib_name, lib_conf)
            
            # Monkey-patch Python's import system
            sys.modules[lib_name] = safe_mod