from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cvsx2mvsx.models.server.structure.timeframe import StructureTimeframe


class StructureEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    timeframes: dict[int, StructureTimeframe]
