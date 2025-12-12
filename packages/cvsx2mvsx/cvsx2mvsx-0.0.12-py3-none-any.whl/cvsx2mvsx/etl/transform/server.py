# import io
# import json
# from uuid import UUID, uuid4
# from zipfile import ZipFile

# import numpy as np

# from cvsx2mvsx.models.internal.entry import InternalEntry


# def make_id(*args):
#     return "::".join(str(x) for x in args).replace(" ", "_")


# class ServerLoader:
#     def __init__(self, internal_entry: InternalEntry):
#         self.internal_entry = internal_entry

#     def load(self) -> UUID:
#         entry_id = uuid4()

#         structure = StructureEntry(id=entry_id)
#         annotation = AnnotationStateRequest()
#         annotation.state[make_id("entry", entry_id)] = EntryAnnotation(name=mvsx.name)

#         with ZipFile(cvsx.filepath, "r") as zf:
#             for timeframe_id, timeframe in mvsx.timeframes.items():
#                 tf_structure = self._process_timeframe(
#                     zf, entry_id, timeframe_id, timeframe, annotation
#                 )
#                 structure.timeframes[timeframe_id] = tf_structure

#         self._store_in_db(entry_id, structure, annotation)
#         return entry_id

#     def _process_timeframe(self, zf, entry_id, timeframe_id, timeframe, annotation):
#         tf_structure = StructureTimeframe(timeframe_id=timeframe_id)

#         annotation.state[make_id("tf", timeframe_id)] = TimeframeAnnotation(
#             name=f"Timeframe {timeframe_id}"
#         )

#         for channel_id, volume in timeframe.volumes.items():
#             self._process_volume(
#                 zf, entry_id, timeframe_id, channel_id, volume, tf_structure, annotation
#             )

#         for seg_id, seg in timeframe.segmentations.items():
#             struct_seg = self._process_segmentation(
#                 zf, entry_id, timeframe_id, seg_id, seg, annotation
#             )
#             tf_structure.segmentations[seg_id] = struct_seg

#         return tf_structure

#     def _process_volume(
#         self, zf, entry_id, timeframe_id, channel_id, volume, tf_structure, annotation
#     ):
#         storage_key = f"entries/{entry_id}/{timeframe_id}/volumes/{channel_id}.bcif"

#         with zf.open(volume.source_filepath) as f:
#             self._upload(storage_key, f.read(), "application/octet-stream")

#         if volume.kind == "isosurface":
#             tf_structure.volumes[channel_id] = StructureIsosurfaceVolume(
#                 timeframe_id=timeframe_id,
#                 channel_id=channel_id,
#                 storage_key=storage_key,
#             )
#         else:
#             tf_structure.volumes[channel_id] = StructureGridSliceVolume(
#                 timeframe_id=timeframe_id,
#                 channel_id=channel_id,
#                 storage_key=storage_key,
#             )

#         annotation.state[make_id("vol", timeframe_id, channel_id)] = VolumeAnnotation(
#             kind="volume",
#             type=volume.kind,
#             color=volume.color,
#             opacity=volume.opacity,
#             relative_isovalue=volume.relative_isovalue,
#         )

#     def _process_segmentation(
#         self, zf, entry_id, timeframe_id, seg_id, seg, annotation
#     ):
#         struct_seg = self._make_segmentation_container(timeframe_id, seg_id, seg)

#         geometric_batch = {}

#         for segment_id_int, segment in seg.segments.items():
#             segment_id = str(segment_id_int)
#             annot_key = make_id("seg", timeframe_id, seg_id, segment_id)

#             if seg.kind == "mesh":
#                 self._process_mesh_segment(
#                     zf,
#                     entry_id,
#                     timeframe_id,
#                     seg_id,
#                     segment_id_int,
#                     segment,
#                     struct_seg,
#                     annotation,
#                     annot_key,
#                 )
#             else:
#                 self._process_geometric_segment(
#                     segment_id_int,
#                     segment,
#                     struct_seg,
#                     annotation,
#                     annot_key,
#                     geometric_batch,
#                 )

#         if seg.kind == "geometric":
#             self._finalize_geometric_batch(
#                 entry_id, timeframe_id, seg_id, struct_seg, geometric_batch
#             )

#         return struct_seg

#     def _make_segmentation_container(self, timeframe_id, seg_id, seg):
#         if seg.kind == "volume":
#             return StructureVolumeSegmentation(timeframe_id, seg_id)
#         elif seg.kind == "mesh":
#             return StructureMeshSegmentation(timeframe_id, seg_id)
#         else:
#             return StructureGeometricSegmentation(timeframe_id, seg_id)

#     def _process_mesh_segment(
#         self,
#         zf,
#         entry_id,
#         timeframe_id,
#         seg_id,
#         segment_id_int,
#         segment,
#         struct_seg,
#         annotation,
#         annot_key,
#     ):
#         segment_id = str(segment_id_int)
#         storage_key = f"entries/{entry_id}/{timeframe_id}/segmentations/{seg_id}/{segment_id}.json"

#         mesh_json = {
#             "vertices": self._flatten(segment.vertices),
#             "indices": self._flatten(segment.indices),
#             "triangle_groups": self._flatten(segment.triangle_groups),
#         }
#         self._upload_json(storage_key, mesh_json)

#         struct_seg.segments[segment_id_int] = StructureMeshSegment(
#             timeframe_id=timeframe_id,
#             segmentation_id=seg_id,
#             segment_id=segment_id_int,
#             storage_key=storage_key,
#         )

#         annotation.state[annot_key] = SegmentAnnotation(
#             kind="segment",
#             type="mesh",
#             color=segment.color,
#             opacity=segment.opacity,
#         )

#     def _process_geometric_segment(
#         self, segment_id_int, segment, struct_seg, annotation, annot_key, batch
#     ):
#         segment_id = str(segment_id_int)

#         batch[segment_id] = segment.model_dump(exclude_none=True, mode="json")

#         struct_seg.segments[segment_id] = self._make_geometric_segment(
#             struct_seg.timeframe_id, struct_seg.segmentation_id, segment_id_int, segment
#         )

#         annotation.state[annot_key] = SegmentAnnotation(
#             kind="segment",
#             type="geometric",
#             color=segment.color,
#             opacity=segment.opacity,
#         )

#     def _make_geometric_segment(self, timeframe_id, seg_id, seg_int, segment):
#         if segment.kind == "box":
#             return StructureBoxSegment(timeframe_id, seg_id, seg_int)
#         if segment.kind == "ellipsoid":
#             return StructureEllipsoidSegment(timeframe_id, seg_id, seg_int)
#         if segment.kind == "sphere":
#             return StructureSphereSegment(timeframe_id, seg_id, seg_int)
#         if segment.kind == "tube":
#             return StructureTubeSegment(timeframe_id, seg_id, seg_int)
#         raise ValueError(f"Unknown geometric segment kind: {segment.kind}")

#     def _finalize_geometric_batch(
#         self, entry_id, timeframe_id, seg_id, struct_seg, batch
#     ):
#         storage_key = f"entries/{entry_id}/{timeframe_id}/segmentations/{seg_id}.json"
#         self._upload_json(storage_key, batch)
#         struct_seg.storage_key = storage_key

#     def _store_in_db(self, entry_id, structure, annotation):
#         db_entry = EntryModel(
#             id=entry_id,
#             structure=structure.model_dump(mode="json"),
#             annotations=annotation.model_dump(mode="json"),
#         )
#         self.db.add(db_entry)
#         self.db.commit()

#     def _upload(self, key, data, content_type):
#         self.minio.put_object(
#             self.bucket, key, io.BytesIO(data), len(data), content_type=content_type
#         )

#     def _upload_json(self, key, data):
#         json_bytes = json.dumps(data).encode("utf-8")
#         self._upload(key, json_bytes, "application/json")

#     def _flatten(self, arr):
#         return arr.ravel().tolist() if isinstance(arr, np.ndarray) else arr
