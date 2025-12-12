from typing import Literal

from pydantic import BaseModel


class TimeframeAnnotation(BaseModel):
    kind: Literal["timeframe"] = "timeframe"

    name: str | None = None
    description: str | None = None
