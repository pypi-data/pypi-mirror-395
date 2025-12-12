"""Parsing utilities for CLI arguments."""

from typing import overload


@overload
def parse_columns(columns: str) -> list[str]: ...
@overload
def parse_columns(columns: None) -> None: ...
def parse_columns(columns: str | None) -> list[str] | None:
    """Parse a comma-separated string of column names into a list, or None if input is None."""
    if columns is None:
        return None
    return [col.strip() for col in columns.split(",")]
