"""MolViewSpec"""

__version__ = "1.8.0"

from cvsx2mvsx.molviewspec.builder import create_builder
from cvsx2mvsx.molviewspec.molstar_widgets import (
    molstar_html,
    molstar_notebook,
    molstar_streamlit,
)
from cvsx2mvsx.molviewspec.mvsx_converter import mvsj_to_mvsx
from cvsx2mvsx.molviewspec.nodes import (
    MVSJ,
    MVSX,
    CategoricalPalette,
    ComponentExpression,
    ContinuousPalette,
    DiscretePalette,
    GlobalMetadata,
    MVSData,
    PrimitiveComponentExpressions,
    Snapshot,
    SnapshotMetadata,
    State,
    States,
    validate_state_tree,
)
