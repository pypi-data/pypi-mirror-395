import os
from tempfile import TemporaryDirectory
from typing import Any

from cvsx2mvsx.etl.pipelines.config import PipelineConfig


class PipelineContext:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self._temp_dir = TemporaryDirectory()
        self.work_dir = self._temp_dir.name
        self.store: dict[str, Any] = {}

    def get_path(self, subpath: str) -> str:
        full_path = os.path.join(self.work_dir, subpath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        return full_path

    def cleanup(self):
        self._temp_dir.cleanup()
