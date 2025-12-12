from typing import Literal

from pydantic import BaseModel


class ServerEntryAnnotation(BaseModel):
    kind: Literal["entry"] = "entry"

    name: str | None = None
    description: str | None = None
