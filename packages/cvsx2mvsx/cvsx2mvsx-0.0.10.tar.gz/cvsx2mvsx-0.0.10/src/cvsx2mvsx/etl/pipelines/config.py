from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    input_path: str
    output_path: str
    lattice_to_mesh: bool = Field(default=False)
