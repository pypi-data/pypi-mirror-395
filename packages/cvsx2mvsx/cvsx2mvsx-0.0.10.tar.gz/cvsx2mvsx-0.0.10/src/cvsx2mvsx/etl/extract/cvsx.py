import json
import os
from typing import Type, TypeVar
from zipfile import BadZipFile, ZipFile

from pydantic import ValidationError

from cvsx2mvsx.etl.extract.parsers.geometric import GeometricParser
from cvsx2mvsx.etl.extract.parsers.lattice import LatticeParser
from cvsx2mvsx.etl.extract.parsers.mesh import MeshParser
from cvsx2mvsx.etl.extract.parsers.volume import VolumeParser
from cvsx2mvsx.models.cvsx.annotations import CVSXAnnotations
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.cvsx.index import CVSXIndex
from cvsx2mvsx.models.cvsx.metadata import CVSXMetadata
from cvsx2mvsx.models.cvsx.proxy import CVSXFilesProxy, FileProxy
from cvsx2mvsx.models.cvsx.query import CVSXQuery

T = TypeVar("T")


class CVSXExtractor:
    INDEX_PATH = "index.json"

    def __init__(self, zip_path: str, out_dir_path: str) -> None:
        self._zip_path = zip_path
        self._out_dir_path = out_dir_path

    def run(self) -> CVSXEntry:
        # extract cvsx archive
        self._extract_all()

        # check that index.json file exists
        index_path = os.path.join(self._out_dir_path, self.INDEX_PATH)
        if not os.path.exists(index_path):
            raise FileNotFoundError("CVSX archive is missing 'index.json'")

        # load index.json
        cvsx_index = self._load_model_from_dir(
            self._out_dir_path,
            self.INDEX_PATH,
            CVSXIndex,
        )

        # check all info and raw data files exist
        self._check_all_files_in_index(self._out_dir_path, cvsx_index)

        # load info files
        cvsx_annotations = self._load_model_from_dir(
            self._out_dir_path,
            cvsx_index.annotations,
            CVSXAnnotations,
        )
        cvsx_metadata = self._load_model_from_dir(
            self._out_dir_path,
            cvsx_index.metadata,
            CVSXMetadata,
        )
        cvsx_query = self._load_model_from_dir(
            self._out_dir_path,
            cvsx_index.query,
            CVSXQuery,
        )

        # load raw data files
        files_proxy = self._load_proxy_models(cvsx_index)

        return CVSXEntry(
            index=cvsx_index,
            annotations=cvsx_annotations,
            metadata=cvsx_metadata,
            query=cvsx_query,
            assets_directory=self._out_dir_path,
            files_proxy=files_proxy,
        )

    def _extract_all(self) -> None:
        if not os.path.exists(self._zip_path):
            raise FileNotFoundError(f"ZIP archive not found: '{self._zip_path}'")
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

    def _load_model_from_dir(
        self,
        base_dir: str,
        inner_path: str,
        model_class: Type[T],
    ) -> T:
        full_path = os.path.join(base_dir, inner_path)

        try:
            with open(full_path, "r") as f:
                json_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in '{full_path}': {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Missing file: '{full_path}'")

        try:
            return model_class.model_validate(json_data)
        except ValidationError as e:
            raise ValueError(f"Invalid data format in '{full_path}': {e}")

    def _check_all_files_in_index(self, base_dir: str, cvsx_index: CVSXIndex) -> None:
        expected_files = set()

        expected_files.update(
            [
                cvsx_index.annotations,
                cvsx_index.metadata,
                cvsx_index.query,
            ]
        )
        expected_files.update(cvsx_index.volumes.keys())

        if cvsx_index.latticeSegmentations:
            expected_files.update(cvsx_index.latticeSegmentations.keys())
        if cvsx_index.geometricSegmentations:
            expected_files.update(cvsx_index.geometricSegmentations.keys())
        if cvsx_index.meshSegmentations:
            for mesh_info in cvsx_index.meshSegmentations:
                expected_files.update(mesh_info.segmentsFilenames)

        for file in expected_files:
            full_path = os.path.join(base_dir, file)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File missing from directory: '{file}'")

    def _load_proxy_models(self, cvsx_index: CVSXIndex) -> None:
        volume_proxies = []
        lattice_proxies = []
        mesh_proxies = []
        geometric_proxies = []

        # volumes
        for filepath, metadata in cvsx_index.volumes.items():
            volume_proxies.append(
                FileProxy(
                    filepath=os.path.join(self._out_dir_path, filepath),
                    metadata=metadata,
                    parser=VolumeParser(),
                )
            )

        # lattice segmentations
        if cvsx_index.latticeSegmentations:
            for filepath, metadata in cvsx_index.latticeSegmentations.items():
                lattice_proxies.append(
                    FileProxy(
                        filepath=os.path.join(self._out_dir_path, filepath),
                        metadata=metadata,
                        parser=LatticeParser(),
                    )
                )

        # geometric segmentations
        if cvsx_index.geometricSegmentations:
            for filepath, metadata in cvsx_index.geometricSegmentations.items():
                geometric_proxies.append(
                    FileProxy(
                        filepath=os.path.join(self._out_dir_path, filepath),
                        metadata=metadata,
                        parser=GeometricParser(),
                    )
                )

        # mesh segmentations
        if cvsx_index.meshSegmentations:
            for metadata in cvsx_index.meshSegmentations:
                for filepath in metadata.segmentsFilenames:
                    mesh_proxies.append(
                        FileProxy(
                            filepath=os.path.join(self._out_dir_path, filepath),
                            metadata=metadata,
                            parser=MeshParser(),
                        )
                    )

        return CVSXFilesProxy(
            volumes=volume_proxies,
            lattice_segmentations=lattice_proxies,
            mesh_segmentations=mesh_proxies,
            geometric_segmentations=geometric_proxies,
        )
