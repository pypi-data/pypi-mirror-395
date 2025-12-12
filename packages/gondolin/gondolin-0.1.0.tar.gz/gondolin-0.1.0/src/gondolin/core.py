import types
import importlib

class SafeProxy:
    def __init__(self, target, policies, registry, prefix=""):
        self._target = target
        self._policies = policies
        self._registry = registry
        self._prefix = prefix

    def _apply_decorators(self, func, rule_list):
        wrapped = func
        for rule in reversed(rule_list):
            if isinstance(rule, str):
                dec = self._registry.get(rule)
                wrapped = dec(wrapped)
            elif isinstance(rule, dict):
                name, arg = list(rule.items())[0]
                dec_factory = self._registry.get(name)
                wrapped = dec_factory(arg)(wrapped)
        return wrapped

    def __getattr__(self, name):
        path = f"{self._prefix}.{name}" if self._prefix else name
        
        # Check Allowlist
        is_exact = path in self._policies
        is_parent = any(k.startswith(path + ".") for k in self._policies.keys())

        if not (is_exact or is_parent):
            raise PermissionError(f"Gondolin Security: Access to '{path}' is denied.")

        real_attr = getattr(self._target, name)

        if is_exact:
            return self._apply_decorators(real_attr, self._policies[path])
        
        return SafeProxy(real_attr, self._policies, self._registry, path)

class ModuleBuilder:
    def __init__(self, registry):
        self.registry = registry

    def create_safe_module(self, lib_name, config):
        # Hidden import of the real library
        real_lib = importlib.import_module(lib_name)
        safe_mod = types.ModuleType(lib_name)
        
        if "target_class" in config:
            cls_name = config["target_class"]
            RealClass = getattr(real_lib, cls_name)
            
            def factory_wrapper(*args, **kwargs):
                instance = RealClass(*args, **kwargs)
                return SafeProxy(instance, config["policies"], self.registry)
            
            setattr(safe_mod, cls_name, factory_wrapper)
            
        return safe_mod