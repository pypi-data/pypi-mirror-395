from HowdenPipeline.flow.parameter_serializer import ParameterSerializer
from typing import Any, Optional
import json
import hashlib

class StepHasher:
    def __init__(self, serializer: Optional[ParameterSerializer] = None) -> None:
        self._serializer = serializer or ParameterSerializer()

    def compute_hash(self, step: Any = None, dependencies: Any = None) -> str:

        if dependencies is not None:
            value = [dep.hashed for dep in dependencies]
        else:
            value = []

        if step is not None:
            value.append(step.hashed)

        serializable = self._serializer.make_serializable(value)
        attrs_str = json.dumps(serializable, sort_keys=True, ensure_ascii=True)
        hashed = hashlib.sha256(attrs_str.encode()).hexdigest()[:8]
        return hashed