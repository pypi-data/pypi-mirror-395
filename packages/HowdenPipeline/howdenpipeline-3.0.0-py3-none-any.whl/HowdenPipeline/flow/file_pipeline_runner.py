import json
from pathlib import Path
from typing import Any, List, Optional
import shutil
import networkx as nx

from HowdenPipeline.flow.parameter_serializer import ParameterSerializer
from HowdenPipeline.flow.match import Match
from HowdenPipeline.flow.pipeline_graph_manager import PipelineNodeData

class FilePipelineRunner:
    def __init__(
            self,
            graph: nx.DiGraph,
            serializer: Optional[ParameterSerializer] = None,
            match_holder: Optional[List[Match]] = None,
            recalculate_all_result: bool = None,
    ) -> None:
        self.graph = graph
        self.serializer = serializer or ParameterSerializer()
        self.match_holder = match_holder if match_holder is not None else []
        self.recalculate_all_result = recalculate_all_result

    def run_for_file(self, file_path: Path) -> dict:
        print(f"Processing {file_path}")
        base_path = Path(file_path.parent)
        for node in self._traversal_order():
            node_data: PipelineNodeData = self.graph.nodes[node]["data"]

            input_file_path = file_path if len(str(node_data.input_file_paths[0])) == 1 else base_path / node_data.input_file_paths[0]
            extra_input = base_path / node_data.input_file_paths[1] if len(node_data.input_file_paths) > 1 else None
            output_folder_file_path = base_path / node_data.output_file_path

            if self.recalculate_all_result or not output_folder_file_path.exists():
                self.delete_folder(Path(output_folder_file_path.parent))
                output_folder_file_path.parent.mkdir(parents=True, exist_ok=True)
                node_data.step.write_json_hyperparameter(Path(output_folder_file_path.parent) / "parameter.json")
                result = self._run_step(node_data.step, input_file_path, extra_input)
                output_folder_file_path.write_text(result, encoding="utf-8")
            else:
                print("    result file already exist")

            if node_data.track:
                path = file_path.parent
                match = Match(
                    result=output_folder_file_path,
                    ground_truth=Path(f"{path}/GT_{node_data.step.name}.json"),
                )
                self.match_holder.append(match)

        return self.graph.graph["result"]

    @staticmethod
    def _run_step(step: Any, input_data: Path, extra_input: Path = None) -> str:

        result = step(input_data, extra_input) if extra_input else step(input_data)

        return result


    def _traversal_order(self) -> List[str]:
        return list(nx.topological_sort(self.graph))

    def _write_parameters(self, step: Any, folder_path: Path) -> None:
        json_parameter = folder_path / "parameter.json"
        attrs = {
            k: v
            for k, v in step.__dict__.items()
            if not k.startswith("_") and k not in ("client", "provider")
        }
        serializable_attrs = self.serializer.make_serializable(attrs)
        json_parameter.write_text(
            json.dumps(
                serializable_attrs,
                indent=2,
                sort_keys=True,
                ensure_ascii=True,
            ),
            encoding="utf-8",
        )
    @staticmethod
    def delete_folder(path: Path) -> None:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
