"""Validation utilities for dataframe operations."""

from typing import overload

import pandas as pd

from pandas_term.core.parsing import parse_columns


def validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Validate that all columns exist in the dataframe."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {', '.join(missing)}")


@overload
def get_columns(df: pd.DataFrame, columns: str) -> list[str]: ...
@overload
def get_columns(df: pd.DataFrame, columns: None) -> None: ...
def get_columns(df: pd.DataFrame, columns: str | None) -> list[str] | None:
    """Parse comma-separated columns and validate they exist in the dataframe."""
    if columns is None:
        return None
    cols = parse_columns(columns)
    validate_columns(df, cols)
    return cols
