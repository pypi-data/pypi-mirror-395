from pydantic import BaseModel

from cvsx2mvsx.models.internal.timeframe import InternalTimeframe


class InternalEntry(BaseModel):
    name: str | None = None
    details: str | None = None
    source_db_id: str | None = None
    source_db_name: str | None = None
    description: str | None = None
    url: str | None = None

    assets_directory: str

    timeframes: dict[int, InternalTimeframe]
