"""Validation utilities for dataframe operations."""

import pandas as pd


def validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Validate that all columns exist in the dataframe."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {', '.join(missing)}")
