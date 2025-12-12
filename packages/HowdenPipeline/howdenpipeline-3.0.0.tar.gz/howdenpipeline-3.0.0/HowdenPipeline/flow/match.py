from dataclasses import dataclass
from pathlib import Path

@dataclass
class Match:
    result: Path
    ground_truth: Path
