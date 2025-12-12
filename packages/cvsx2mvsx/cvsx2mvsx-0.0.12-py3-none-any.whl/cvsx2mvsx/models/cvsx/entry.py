from typing import TypeVar

from pydantic import BaseModel

from cvsx2mvsx.models.cvsx.annotations import CVSXAnnotations
from cvsx2mvsx.models.cvsx.index import CVSXIndex
from cvsx2mvsx.models.cvsx.metadata import CVSXMetadata
from cvsx2mvsx.models.cvsx.proxy import CVSXFilesProxy
from cvsx2mvsx.models.cvsx.query import CVSXQuery

T = TypeVar("T")


class CVSXEntry(BaseModel):
    index: CVSXIndex
    annotations: CVSXAnnotations
    metadata: CVSXMetadata
    query: CVSXQuery

    assets_directory: str
    files_proxy: CVSXFilesProxy
