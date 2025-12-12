from pydantic import BaseModel

from cvsx2mvsx.models.server.annotation.state import AnnotationState
from cvsx2mvsx.models.server.structure.entry import StructureEntry


class ServerEntry(BaseModel):
    structure: StructureEntry
    annotations: AnnotationState
