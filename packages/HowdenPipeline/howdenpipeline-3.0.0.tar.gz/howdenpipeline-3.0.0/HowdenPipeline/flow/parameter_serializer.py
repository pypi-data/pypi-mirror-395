from typing import Any

class ParameterSerializer:
    def make_serializable(self, obj: Any) -> Any:
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, (list, tuple, set)):
            return [self.make_serializable(v) for v in obj]
        if isinstance(obj, dict):
            return {k: self.make_serializable(v) for k, v in sorted(obj.items())}
        if hasattr(obj, "__dict__"):
            return self.make_serializable(vars(obj))
        return f"{type(obj).__name__}:{repr(obj)}"