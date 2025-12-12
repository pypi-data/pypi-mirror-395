import gc
import os
from zipfile import ZIP_DEFLATED, ZipFile

from cvsx2mvsx.models.mvsx.states import MVSXEntry


class MVSXLoader:
    INDEX_PATH = "index.mvsj"

    def __init__(
        self,
        mvsx_entry: MVSXEntry,
        out_file_path: str,
        compression_level: int,
    ) -> None:
        self._mvsx_entry = mvsx_entry
        self._out_file_path = out_file_path
        self._compression_level = compression_level

    def run(self) -> None:
        gc.collect()

        dirpath = os.path.dirname(self._out_file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with ZipFile(
            self._out_file_path,
            mode="w",
            compression=ZIP_DEFLATED,
            compresslevel=self._compression_level,
        ) as z:
            data = self._mvsx_entry.states.model_dump_json(exclude_none=True, indent=2)
            z.writestr(self.INDEX_PATH, data)
            for root, dirs, files in os.walk(self._mvsx_entry.asset_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(
                        full_path, self._mvsx_entry.asset_dir
                    )
                    z.write(full_path, arcname=relative_path)
