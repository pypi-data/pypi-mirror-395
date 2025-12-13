from collections import defaultdict

from cvsx2mvsx.etl.transform.geometric import GeometricTransformer
from cvsx2mvsx.etl.transform.lattice import LatticeTransformer
from cvsx2mvsx.etl.transform.mesh import MeshTransformer
from cvsx2mvsx.etl.transform.volume import VolumeTransformer
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.internal.entry import InternalEntry
from cvsx2mvsx.models.internal.segmentation import InternalSegmentation
from cvsx2mvsx.models.internal.timeframe import InternalTimeframe


class InternalTransformer:
    def __init__(
        self,
        cvsx_entry: CVSXEntry,
        out_dir_path: str,
        lattice_to_mesh: bool,
    ) -> None:
        self._cvsx_entry = cvsx_entry
        self._out_dir_path = out_dir_path
        self._lattice_to_mesh = lattice_to_mesh

    def run(self) -> InternalEntry:
        # transform all volumes and segmentations
        volumes = VolumeTransformer(
            cvsx_entry=self._cvsx_entry,
            out_dir_path=self._out_dir_path,
        ).run()
        lattice_segmentations = LatticeTransformer(
            cvsx_entry=self._cvsx_entry,
            out_dir_path=self._out_dir_path,
            lattice_to_mesh=self._lattice_to_mesh,
        ).run()
        mesh_segmentations = MeshTransformer(
            cvsx_entry=self._cvsx_entry,
            out_dir_path=self._out_dir_path,
        ).run()
        geometric_segmentations = GeometricTransformer(
            cvsx_entry=self._cvsx_entry,
            out_dir_path=self._out_dir_path,
        ).run()

        segmentations: list[InternalSegmentation] = (
            lattice_segmentations + mesh_segmentations + geometric_segmentations
        )

        # group by timeframe id
        grouped = defaultdict(lambda: {"volumes": {}, "segmentations": {}})
        for vol in volumes:
            grouped[vol.timeframe_id]["volumes"][vol.channel_id] = vol
        for seg in segmentations:
            grouped[seg.timeframe_id]["segmentations"][seg.segmentation_id] = seg

        timeframe_models: dict[int, InternalTimeframe] = {}
        for tf_id in sorted(grouped.keys()):
            data = grouped[tf_id]
            timeframe_models[tf_id] = InternalTimeframe(
                timeframe_id=tf_id,
                volumes=data["volumes"].values(),
                segmentations=data["segmentations"].values(),
            )

        return InternalEntry(
            timeframes=timeframe_models.values(),
            assets_directory=self._out_dir_path,
        )
