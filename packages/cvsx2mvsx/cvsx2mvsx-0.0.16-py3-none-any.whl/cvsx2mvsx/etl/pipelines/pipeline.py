from typing import Any

from cvsx2mvsx.etl.pipelines.config import PipelineConfig
from cvsx2mvsx.etl.pipelines.context import PipelineContext
from cvsx2mvsx.etl.pipelines.pipeline_steps import PipelineStep


class Pipeline:
    def __init__(self, steps: list[PipelineStep]):
        self._steps = steps

    def run(self, config: PipelineConfig) -> Any:
        context = PipelineContext(config)
        current_data = config.input_path

        try:
            for step in self._steps:
                current_data = step.execute(current_data, context)
            return current_data
        finally:
            context.cleanup()
