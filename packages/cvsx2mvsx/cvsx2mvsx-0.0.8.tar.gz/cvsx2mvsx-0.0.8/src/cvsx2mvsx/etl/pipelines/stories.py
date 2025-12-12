import os
from tempfile import TemporaryDirectory

from cvsx2mvsx.etl.extract.cvsx import CVSXExtractor
from cvsx2mvsx.etl.load.stories import StoriesLoader
from cvsx2mvsx.etl.transform.internal import InternalTransformer
from cvsx2mvsx.etl.transform.stories import StoriesTransformer


class CvsxToStoriesPipeline:
    def __init__(
        self,
        cvsx_path: str,
        output_path: str,
        lattice_to_mesh: bool = True,
    ) -> None:
        self._cvsx_path = cvsx_path
        self._output_path = output_path
        self._lattice_to_mesh = lattice_to_mesh

    def run(self) -> None:
        with TemporaryDirectory() as tempdir:
            cvsx_dir = f"{tempdir}/cvsx"
            internal_dir = f"{tempdir}/internal"
            mvsx_dir = f"{tempdir}/mvsx"

            for dirpath in [cvsx_dir, internal_dir, mvsx_dir]:
                if not dirpath:
                    continue
                os.makedirs(dirpath, exist_ok=True)

            cvsx_entry = CVSXExtractor(
                zip_path=self._cvsx_path,
                out_dir_path=cvsx_dir,
            ).run()

            internal_entry = InternalTransformer(
                cvsx_entry=cvsx_entry,
                out_dir_path=internal_dir,
                lattice_to_mesh=self._lattice_to_mesh,
            ).run()

            story_container = StoriesTransformer(
                internal_entry=internal_entry,
            ).run()

            StoriesLoader(
                story_container=story_container,
                out_file_path=self._output_path,
            ).run()
