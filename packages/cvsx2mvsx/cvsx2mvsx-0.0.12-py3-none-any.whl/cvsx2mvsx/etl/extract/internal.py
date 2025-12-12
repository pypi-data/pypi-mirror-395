import json
import os

from cvsx2mvsx.models.internal.entry import InternalEntry


class InternalExtractor:
    def __init__(self, internal_dir_path: str) -> None:
        self._internal_dir_path = internal_dir_path

    def run(self) -> InternalEntry:
        json_path = os.path.join(self._internal_dir_path, "internal.json")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Internal model index not found at: {json_path}")

        with open(json_path, "r") as f:
            data = json.load(f)

        try:
            entry = InternalEntry.model_validate(data)
        except Exception as e:
            raise ValueError(f"Failed to parse internal.json: {e}")

        entry.assets_directory = self._internal_dir_path

        return entry
