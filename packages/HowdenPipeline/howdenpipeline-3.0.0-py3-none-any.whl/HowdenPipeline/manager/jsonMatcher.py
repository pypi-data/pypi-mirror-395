from dataclasses import dataclass
from pathlib import Path
import json
from typing import List, Dict, Any
from collections import defaultdict


@dataclass
class Match:
    result: Path
    ground_truth: Path


@dataclass
class Information:
    file1_path: str
    file2_path: str
    filename: str
    accuracy: float
    total_keys: int
    matched_keys: int
    mismatches: int


class JsonMatcher:
    """Compare JSON files and compute match accuracy."""

    def __init__(self, matches: List[Match]):
        #self.matches = matches
        self.infos = self.run(matches)

    # ----------------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------------
    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _flatten_json(data: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(JsonMatcher._flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # ----------------------------------------------------------------------
    # Comparison logic
    # ----------------------------------------------------------------------
    def _compare_pair(self, file1: Path, file2: Path) -> Information:
        json1 = self._flatten_json(self._load_json(file1))
        json2 = self._flatten_json(self._load_json(file2))

        all_keys = set(json1.keys()) | set(json2.keys())
        total = len(all_keys)
        correct = 0
        mismatches = 0

        for key in all_keys:
            v1 = json1.get(key)
            v2 = json2.get(key)
            if v1 == v2 and v1 is not None:
                correct += 1
            else:
                mismatches += 1

        accuracy = correct / total if total else 1.0

        # Extract top level filename (folder name before underscore)
        filename = file1.parent.name.split("_")[0]

        return Information(
            file1_path=str(file1),
            file2_path=str(file2),
            filename=filename,
            accuracy=round(accuracy, 4),
            total_keys=total,
            matched_keys=correct,
            mismatches=mismatches,
        )

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def run(self, matches):
        """Run comparisons for all match pairs."""
        return [self._compare_pair(m.result, m.ground_truth) for m in matches]


    def report(self):
        """Pretty-print comparison results."""

        for info in self.infos:
            print(f"\nComparing: {info.file1_path} ↔ {info.file2_path}")
            print(f"Filename: {info.filename}")
            print(f"Accuracy: {info.accuracy * 100:.2f}% ({info.matched_keys}/{info.total_keys})")
            print(f"Mismatches: {info.mismatches}")

        avg_accuracy = sum(i.accuracy for i in self.infos) / len(self.infos)
        print(f"\nOverall average accuracy: {avg_accuracy * 100:.2f}%")


    # ----------------------------------------------------------------------
    # Combined accuracy per filename
    # ----------------------------------------------------------------------
    def get_accuracy_per_filename(self) -> Dict[str, float]:
        """Compute weighted accuracy across all comparisons grouped by filename."""
        groups = defaultdict(list)

        for info in self.infos:
            groups[info.filename].append(info)

        results = {}

        for filename, items in groups.items():
            total_keys = sum(i.total_keys for i in items)

            weighted_sum = sum(i.accuracy * i.total_keys for i in items)
            combined_accuracy = weighted_sum / total_keys

            results[f"accuracy_{filename}"] = round(combined_accuracy * 100, 2)

        return results
