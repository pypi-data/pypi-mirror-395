class Registry:
    def __init__(self):
        self._store = {}

    def register(self, name):
        def inner(func):
            self._store[name] = func
            return func
        return inner

    def get(self, name):
        if name not in self._store:
            raise ValueError(f"Policy '{name}' is not defined in the Registry.")
        return self._store[name]