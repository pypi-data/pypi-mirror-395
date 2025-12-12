import sys
import unittest
from types import ModuleType
from typing import Callable, cast, override

from gondolin.module_builder import LibConfig, ModuleBuilder
from gondolin.safe_proxy import Policies, Rule, SafeProxy
from gondolin.registry import Registry

# --- Mocks for Testing ---

class SubSystem:
    def deep_action(self) -> str:
        return "deep_success"

    def deep_danger(self) -> str:
        return "deep_fail"

class MockTarget:
    """A fake library class to wrap."""

    sub: SubSystem

    def __init__(self):
        self.sub = SubSystem()

    def safe_action(self, x: int) -> int:
        return x * 2

    def dangerous_action(self) -> str:
        return "exploded"

# --- Test Suite ---

class TestGondolin(unittest.TestCase):

    registry: Registry
    target: MockTarget

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.registry = Registry()
        self.target = MockTarget()

    @override
    def setUp(self) -> None:
        """Runs before every test."""
        self.registry = Registry()
        self.target = MockTarget()

        # Register a simple audit decorator
        def audit(func: Callable[..., object]) -> Callable[..., str]:
            def wrapper(*args: object, **kwargs: object) -> str:
                return f"audited:{func(*args, **kwargs)}"

            return wrapper

        _ = self.registry.register("audit")(audit)

        # Register a parametrized decorator
        def limit(max_val: int) -> Callable[[Callable[[int], int]], Callable[[int], int]]:
            def decorator(func: Callable[[int], int]) -> Callable[[int], int]:
                def wrapper(x: int) -> int:
                    if x > max_val:
                        raise ValueError("Limit exceeded")
                    return func(x)

                return wrapper

            return decorator

        _ = self.registry.register("limit")(limit)

    def test_proxy_blocks_unknown_methods(self):
        """Test that methods not in the policy are blocked."""
        policies: Policies = {
            "safe_action": [cast(Rule, "audit")]
        }
        proxy = SafeProxy(self.target, policies, self.registry)

        safe_action = cast(Callable[[int], str], proxy.safe_action)

        # Should work
        self.assertEqual(safe_action(10), "audited:20")

        # Should fail (not in policy)
        with self.assertRaises(PermissionError):
            _ = proxy.dangerous_action

    def test_recursive_proxy(self):
        """Test that the proxy handles nested objects correctly."""
        policies: Policies = {
            "sub.deep_action": [cast(Rule, "audit")]
        }
        proxy = SafeProxy(self.target, policies, self.registry)

        # 1. Accessing 'sub' should return a NEW SafeProxy (because it's a parent path)
        sub_proxy = cast(SafeProxy, proxy.sub)
        self.assertIsInstance(sub_proxy, SafeProxy)

        # 2. Accessing 'deep_action' should work
        deep_action = cast(Callable[[], str], sub_proxy.deep_action)
        result = deep_action()
        self.assertEqual(result, "audited:deep_success")

        # 3. Accessing 'deep_danger' should fail
        with self.assertRaises(PermissionError):
            deep_danger = cast(Callable[[], str], sub_proxy.deep_danger)
            _ = deep_danger()

    def test_decorator_logic_application(self):
        """Test that decorators are applied in the correct order."""
        policies: Policies = {
            "safe_action": [
                cast(Rule, "audit"),           # Outer wrapper
                {"limit": 5}       # Inner wrapper
            ]
        }
        proxy = SafeProxy(self.target, policies, self.registry)

        safe_action = cast(Callable[[int], str], proxy.safe_action)

        # Case 1: Within limit (2 * 2 = 4, audited -> "audited:4")
        self.assertEqual(safe_action(2), "audited:4")

        # Case 2: Exceeds limit
        with self.assertRaises(ValueError):
            _ = safe_action(10)

    def test_missing_policy_in_registry(self):
        """Test that using an unknown policy name raises an error."""
        policies: Policies = {"safe_action": [cast(Rule, "unknown_decorator")]} 
        proxy = SafeProxy(self.target, policies, self.registry)

        with self.assertRaises(ValueError) as cm:
            safe_action = cast(Callable[[int], str], proxy.safe_action)
            _ = safe_action(1)
        self.assertIn("not defined in the Registry", str(cm.exception))

    def test_module_level_proxy_requires_target_class(self):
        """Validation should fail when target_class is missing."""
        module_name = "dummy_fp_lib"
        fake_mod = ModuleType(module_name)
        sys.modules[module_name] = fake_mod

        try:
            policies: Policies = {"safe_fn": [cast(Rule, "audit")]} 
            lib_conf: LibConfig = {"policies": policies, "target_class": "__module__"}

            builder = ModuleBuilder(self.registry)
            with self.assertRaises(AttributeError):
                _ = builder.create_safe_module(module_name, lib_conf)
        finally:
            _ = sys.modules.pop(module_name, None)

if __name__ == "__main__":
    _ = unittest.main()