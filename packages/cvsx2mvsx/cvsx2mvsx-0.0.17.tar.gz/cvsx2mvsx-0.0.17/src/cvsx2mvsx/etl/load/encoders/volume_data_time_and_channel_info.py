from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cvsx.common import VolumeDataTimeAndChannelInfo


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
                value=lambda d, i: data.time_id,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="channel_id",
                value=lambda d, i: data.channel_id,
                dtype="i4",
            ),
        ]
