from typing import Any

class StepNamer:
    @staticmethod
    def name_for(step: Any) -> str:
        name = getattr(step, "name", None)
        if name:
            return name
        return step.__class__.__name__