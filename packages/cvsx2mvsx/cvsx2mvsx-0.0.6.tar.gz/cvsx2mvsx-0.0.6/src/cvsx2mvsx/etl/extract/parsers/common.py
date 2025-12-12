from typing import Any
from zipfile import ZipFile

import numpy as np
from ciftools.models.data import CIFCategory, CIFDataBlock, CIFFile


def read_file_from_zip(zip_path: str, inner_path: str) -> bytes:
    with ZipFile(zip_path, "r") as f:
        return f.read(inner_path)


def find_block(cif_file: CIFFile, block_name: str) -> CIFDataBlock | None:
    for block in cif_file.data_blocks:
        if block.header == block_name:
            return block


def find_category(cif_block: CIFDataBlock, category_name: str) -> CIFCategory | None:
    for category in cif_block.categories.values():
        if category.name == category_name:
            return category


def has_column(category: CIFCategory, column_name: str) -> bool:
    return column_name in category.field_names


def to_ndarray(category: CIFCategory, column_name: str) -> np.ndarray:
    if not has_column(category, column_name):
        raise ValueError(
            f"Cif category '{category.name}' doesn't have column with name '{column_name}'."
        )
    return category[column_name].as_ndarray()


def to_item(category: CIFCategory, column_name: str) -> list[Any]:
    if not has_column(category, column_name):
        raise ValueError(
            f"Cif category '{category.name}' doesn't have column with name '{column_name}'."
        )
    return category[column_name].as_ndarray().item()
