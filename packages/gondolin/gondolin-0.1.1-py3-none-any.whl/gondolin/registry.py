from typing import Callable

class Registry:
    _store: dict[str, Callable[..., object]]

    def __init__(self):
        self._store = {}

    def register(self, name: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
        """
        Decorator to register a policy function.
        Usage: @registry.register("audit_log")
        """
        def inner(func: Callable[..., object]) -> Callable[..., object]:
            self._store[name] = func
            return func
        return inner

    def get(self, name: str) -> Callable[..., object]:
        """Retrieve a policy by name."""
        if name not in self._store:
            raise ValueError(f"Gondolin Policy '{name}' is not defined in the Registry. Did you forget to register it?")
        return self._store[name]