from molviewspec import States
from pydantic import BaseModel


class MVSXEntry(BaseModel):
    states: States
    asset_dir: str
