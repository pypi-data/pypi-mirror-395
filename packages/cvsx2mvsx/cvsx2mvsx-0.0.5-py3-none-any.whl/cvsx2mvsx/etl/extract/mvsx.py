import json
import os
from zipfile import BadZipFile, ZipFile

from molviewspec import States

from cvsx2mvsx.models.mvsx.states import MVSXEntry


class MVSXExtractor:
    def __init__(
        self,
        zip_path: str,
        out_dir_path: str,
    ) -> None:
        self._zip_path = zip_path
        self._out_dir_path = out_dir_path

    def run(self) -> MVSXEntry:
        # extract mvsx archive
        self._extract_all()

        # check that index.mvsj exists
        index_path = os.path.join(self._out_dir_path, "index.mvsj")
        if not os.path.exists(index_path):
            raise FileNotFoundError("MVSX archive is missing 'index.mvsj'")

        with open(index_path, "r") as f:
            data = json.load(f)

        try:
            states = States.model_validate(data)
        except Exception as e:
            raise ValueError(f"Failed to parse index.mvsj: {e}")

        return MVSXEntry(states=states, asset_dir=self._out_dir_path)

    def _extract_all(self) -> None:
        if not os.path.exists(self._zip_path):
            raise FileNotFoundError(f"MVSX archive not found: '{self._zip_path}'")
        if not os.path.isfile(self._zip_path):
            raise ValueError(f"Path exists but is not a file: '{self._zip_path}'")

        if self._out_dir_path:
            os.makedirs(self._out_dir_path, exist_ok=True)

        try:
            with ZipFile(self._zip_path, "r") as z:
                z.extractall(self._out_dir_path)
        except BadZipFile:
            raise ValueError(
                f"File '{self._zip_path}' is corrupted or not a valid ZIP archive."
            )
        except Exception as e:
            raise RuntimeError(f"Failed to extract zip archive: {e}")
