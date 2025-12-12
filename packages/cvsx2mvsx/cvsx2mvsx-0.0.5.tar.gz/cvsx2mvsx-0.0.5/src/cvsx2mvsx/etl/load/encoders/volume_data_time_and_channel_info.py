from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.common import VolumeDataTimeAndChannelInfo
from cvsx2mvsx.models.cif.write.encoders import bytearray_encoder


class VolumeDataTimeAndChannelInfoCategory(CIFCategoryDesc):
    name = "volume_data_time_and_channel_info"

    @staticmethod
    def get_row_count(data: VolumeDataTimeAndChannelInfo) -> int:
        return 1

    @staticmethod
    def get_field_descriptors(data: VolumeDataTimeAndChannelInfo):
        return [
            CIFFieldDesc.numbers(
                name="time_id",
                value=lambda d: d.time_id,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="channel_id",
                value=lambda d: d.channel_id,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
        ]
