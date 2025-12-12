from pathlib import Path
from typing import Any, Iterable, List, Optional, Callable


from HowdenPipeline.manager.jsonMatcher import JsonMatcher
from HowdenPipeline.manager.tracker import Tracker
from HowdenPipeline.flow.parameter_serializer import ParameterSerializer
from HowdenPipeline.flow.pipeline_graph_manager import PipelineGraphManager
from HowdenPipeline.flow.step_namer import StepNamer
from HowdenPipeline.flow.step_hasher import StepHasher
from HowdenPipeline.flow.match import Match
from HowdenPipeline.flow.file_pipeline_runner import FilePipelineRunner


class GraphPipeline:
    def __init__(
            self,
            pdf = None,
            tracker: Optional[Tracker] = None,
            recalculate_all_result: bool = False,
            graph_manager: Optional[PipelineGraphManager] = None,
            serializer: Optional[ParameterSerializer] = None,
            hasher: Optional[StepHasher] = None,
            namer: Optional[StepNamer] = None,
            matcher_factory: Optional[Callable[[List[Match]], Any]] = None,
            result_file_name: str = "result"
    ) -> None:

        self.recalculate_all_result = recalculate_all_result
        self.result_file_name = result_file_name
        self.file_path_pdf: Path = pdf

        self.serializer = serializer or ParameterSerializer()
        self.hasher = hasher or StepHasher(self.serializer)
        self.namer = namer or StepNamer()

        self.graph_manager = graph_manager or PipelineGraphManager(
            hasher=self.hasher,
            namer=self.namer,
            result_file_name = self.result_file_name

        )

        self.tracker = tracker
        if self.tracker:
            print("run mlflow by writing <mlflow ui> in cli")

        self.matcher_factory = matcher_factory or JsonMatcher
        self.matches: List[Match] = []

    def add_step(
            self,
            step: Any,
            dependencies: Optional[Iterable[Any]] = None,
            track: bool = False,
            filetype: Optional[str] = None,
    ) -> None:


        self.graph_manager.add_step(
            step=step,
            dependencies=dependencies,
            track=track,
            filetype=filetype,
        )

    def execute(self):
        if not self.file_path_pdf:
            return []

        file_pipeline_manager = FilePipelineRunner(
                self.graph_manager.graph.copy(),
                self.serializer,
                self.matches,
                self.recalculate_all_result,
            )
        result = file_pipeline_manager.run_for_file(self.file_path_pdf)

        if self.tracker and self.matcher_factory and self.matches:
            matcher = self.matcher_factory(self.matches)
            self.tracker.log_metrics(matcher.get_accuracy_per_filename())
            self.tracker.log_artifacts("././poetry.lock")
        return result
