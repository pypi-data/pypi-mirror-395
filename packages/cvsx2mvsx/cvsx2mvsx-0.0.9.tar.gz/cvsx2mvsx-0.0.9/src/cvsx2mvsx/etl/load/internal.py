import os
import shutil

from cvsx2mvsx.models.internal.entry import InternalEntry


class InternalLoader:
    INDEX_PATH = "internal.json"

    def __init__(
        self,
        internal_entry: InternalEntry,
        assets_dir: str,
        out_dir_path: str,
    ) -> None:
        self._internal_entry = internal_entry
        self._assets_dir = assets_dir
        self._out_dir_path = out_dir_path

    def run(self) -> None:
        internal_path = os.path.join(self._assets_dir, self.INDEX_PATH)
        with open(internal_path, "w") as f:
            json_output = self._internal_entry.model_dump_json(indent=2)
            f.write(json_output)

        for root, dirs, files in os.walk(self._assets_dir):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, self._assets_dir)
                destination_path = os.path.join(self._out_dir_path, relative_path)
                dirpath = os.path.dirname(destination_path)
                if dirpath:
                    os.makedirs(dirpath, exist_ok=True)
                shutil.move(source_path, destination_path)
