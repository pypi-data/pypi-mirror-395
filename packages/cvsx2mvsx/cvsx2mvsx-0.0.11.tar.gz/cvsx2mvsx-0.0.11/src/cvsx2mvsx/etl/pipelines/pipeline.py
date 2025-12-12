from typing import Any

from cvsx2mvsx.etl.pipelines.config import PipelineConfig
from cvsx2mvsx.etl.pipelines.context import PipelineContext
from cvsx2mvsx.etl.pipelines.steps import Step


class Pipeline:
    def __init__(self, steps: list[Step]):
        self._steps = steps

    def run(self, config: PipelineConfig) -> Any:
        context = PipelineContext(config or {})
        current_data = config.input_path

        try:
            for step in self._steps:
                current_data = step.execute(current_data, context)
            return current_data
        finally:
            context.cleanup()
