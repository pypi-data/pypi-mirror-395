from pydantic import BaseModel


class EntryId(BaseModel):
    source_db_id: str | None
    source_db_name: str | None


class VolumeData3dInfo(BaseModel):
    name: str
    axis_order_0: int
    axis_order_1: int
    axis_order_2: int
    origin_0: float
    origin_1: float
    origin_2: float
    dimensions_0: float
    dimensions_1: float
    dimensions_2: float
    sample_rate: int
    sample_count_0: int
    sample_count_1: int
    sample_count_2: int
    spacegroup_number: int
    spacegroup_cell_size_0: float
    spacegroup_cell_size_1: float
    spacegroup_cell_size_2: float
    spacegroup_cell_angles_0: float
    spacegroup_cell_angles_1: float
    spacegroup_cell_angles_2: float
    mean_source: float
    mean_sampled: float
    sigma_source: float
    sigma_sampled: float
    min_source: float
    min_sampled: float
    max_source: float
    max_sampled: float


class VolumeDataTimeAndChannelInfo(BaseModel):
    time_id: int
    channel_id: int
