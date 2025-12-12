"""Service for reading and writing dataframes from various sources."""

import sys
from pathlib import Path

import pandas as pd


def read_dataframe(input_path: str) -> pd.DataFrame:
    """Read a dataframe from a file path or stdin."""
    if input_path == "-":
        return pd.read_csv(sys.stdin)

    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file format: {suffix}")


def write_dataframe(
    df: pd.DataFrame,
    output_path: str | None = None,
    use_json: bool = False,
) -> None:
    """Write a dataframe to a file path or stdout."""
    if output_path is None or output_path == "-":
        if use_json:
            sys.stdout.write(df.to_json(orient="records", indent=2))
            sys.stdout.write("\n")
        else:
            df.to_csv(sys.stdout, index=False)
        return

    path = Path(output_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        df.to_csv(path, index=False)
    elif suffix in [".xlsx", ".xls"]:
        df.to_excel(path, index=False)
    elif suffix == ".json":
        df.to_json(path, orient="records", indent=2)
    elif suffix == ".parquet":
        df.to_parquet(path, index=False)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
