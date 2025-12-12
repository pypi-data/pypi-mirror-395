import os
from zipfile import ZIP_DEFLATED, ZipFile

from cvsx2mvsx.models.mvsx.states import MVSXEntry


class MVSXLoader:
    def __init__(self, mvsx_entry: MVSXEntry, out_file_path: str) -> None:
        self._mvsx_entry = mvsx_entry
        self._out_file_path = out_file_path

    def run(self) -> None:
        dirpath = os.path.dirname(self._out_file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with ZipFile(self._out_file_path, mode="w", compression=ZIP_DEFLATED) as z:
            data = self._mvsx_entry.states.model_dump_json(exclude_none=True, indent=2)
            z.writestr("index.mvsj", data)
            for root, dirs, files in os.walk(self._mvsx_entry.asset_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(
                        full_path, self._mvsx_entry.asset_dir
                    )
                    z.write(full_path, arcname=relative_path)
