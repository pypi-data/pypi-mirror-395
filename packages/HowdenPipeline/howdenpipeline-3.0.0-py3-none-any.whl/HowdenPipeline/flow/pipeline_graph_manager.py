from typing import Any, Iterable, Optional, List
import networkx as nx
from dataclasses import dataclass
from HowdenPipeline.flow.step_namer import StepNamer
from HowdenPipeline.flow.step_hasher import StepHasher
from pathlib import Path

@dataclass
class PipelineNodeData:
    """
    Holds metadata and runtime information for a pipeline step.

    Attributes:
        step: The callable or object representing the pipeline step.
        name: Human readable name of the step. extract
        track: Indicates whether this step should be tracked.
        filetype: Optional file extension associated with the output.
        result: The computed result from the step, if available.
        hash: Content hash that identifies this step version. (hyperparameter - hashed)
        folder_name: Name of the folder where artifacts are stored. (e.g. extractor_6tv_68xd)
"""

    step: Any
    name: str
    track: bool
    filetype: Optional[str]
    result: Optional[Any]
    hash: str
    folder_name: str
    dependencies: Any
    output_file_path: Path
    input_file_paths: List[Path]


class PipelineGraphManager:
    def __init__(
            self,
            base_graph: Optional[nx.DiGraph] = None,
            hasher: Optional[StepHasher] = None,
            namer: Optional[StepNamer] = None,
            result_file_name: Optional[str] = None,
    ) -> None:
        self.graph: nx.DiGraph = base_graph or nx.DiGraph()
        self._hasher = hasher or StepHasher()
        self._namer = namer or StepNamer()
        self.graph.graph["result"] = {}
        self.graph.graph["result_name_file"] = result_file_name

    def add_step(
            self,
            step: Any,
            dependencies: Optional[Iterable[Any]] = None,
            track: bool = False,
            filetype: Optional[str] = None,
    ) -> None:

        input_file_paths: [Path] = [self.graph.nodes[dep]["data"].output_file_path for dep in dependencies] if dependencies else [Path()]

        node_label: str = self._create_node_name(step.name, self._hasher.compute_hash(step, dependencies))

        output_file_path = self.get_output_path(dependencies, node_label)

        node_data = PipelineNodeData(
            step=step,
            name=step.name,
            track=track,
            filetype=filetype,
            result=None,
            hash=self._hasher.compute_hash(step, dependencies),
            folder_name=node_label,
            input_file_paths=input_file_paths,
            output_file_path=output_file_path,
            dependencies = dependencies
        )

        self.graph.add_node(step, data=node_data)

        #if dep_steps_to_folders:
        #    for dep_label in dependencies:
        #        self.graph.add_edge(dep_label, node_label)

    def get_output_path(self, dependencies: [Any], node_label: str) -> Path:
        if dependencies:
            input_file_paths_hest = []
            for dep in dependencies:
                b = self.graph.nodes[dep]["data"].output_file_path
                input_file_paths_hest.append(str(b))
            longest_path = max(input_file_paths_hest, key=len)
            longest_path = Path(Path(longest_path).parent)
            output_file_path = longest_path / Path(node_label) / Path(self.graph.graph["result_name_file"] + ".md")
        else:
            output_file_path = node_label + "/" + self.graph.graph["result_name_file"] + ".md"
        return output_file_path

    @staticmethod
    def _create_node_name(name:str, hashed: str) -> str:
        return f"{name}_{hashed}"