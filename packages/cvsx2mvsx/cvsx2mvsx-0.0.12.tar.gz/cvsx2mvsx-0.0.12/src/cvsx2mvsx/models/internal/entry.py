from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.internal.timeframe import InternalTimeframe


class InternalEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    details: str | None = None
    source_db_id: str | None = None
    source_db_name: str | None = None
    description: str | None = None
    url: str | None = None

    assets_directory: str

    timeframes: list[InternalTimeframe]
