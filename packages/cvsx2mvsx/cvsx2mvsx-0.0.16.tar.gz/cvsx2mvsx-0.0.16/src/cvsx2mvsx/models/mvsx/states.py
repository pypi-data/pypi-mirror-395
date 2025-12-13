from pydantic import BaseModel

from cvsx2mvsx.molviewspec.nodes import States


class MVSXEntry(BaseModel):
    states: States
    asset_dir: str
