"""CLI commands for dataframe filtering operations."""

from typing import Annotated

import typer

from pandas_term.cli.options import (
    FormatOption,
    InputFileArgument,
    OutputFileOption,
    UseJsonOption,
    get_output_options,
)
from pandas_term.cli.validators import get_columns, positive_int
from pandas_term.core import io_operations

app = typer.Typer(add_completion=False)


@app.command()
def query(
    expression: Annotated[str, typer.Argument(help="Pandas query expression")],
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    fmt: FormatOption = None,
    output: OutputFileOption = None,
) -> None:
    """Filter dataframe using a pandas query expression."""
    df = io_operations.read_dataframe(input_file)
    result = df.query(expression)
    io_operations.write_dataframe(result, get_output_options(use_json, fmt, output))


@app.command()
def head(
    input_file: InputFileArgument = "-",
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows", callback=positive_int)] = 10,
    use_json: UseJsonOption = False,
    fmt: FormatOption = None,
    output: OutputFileOption = None,
) -> None:
    """Return the first n rows of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    result = df.head(n)
    io_operations.write_dataframe(result, get_output_options(use_json, fmt, output))


@app.command()
def tail(
    input_file: InputFileArgument = "-",
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows", callback=positive_int)] = 10,
    use_json: UseJsonOption = False,
    fmt: FormatOption = None,
    output: OutputFileOption = None,
) -> None:
    """Return the last n rows of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    result = df.tail(n)
    io_operations.write_dataframe(result, get_output_options(use_json, fmt, output))


@app.command()
def dropna(
    input_file: InputFileArgument = "-",
    subset: Annotated[
        str | None,
        typer.Option("--subset", "-s", help="Comma-separated columns to check for null values"),
    ] = None,
    use_json: UseJsonOption = False,
    fmt: FormatOption = None,
    output: OutputFileOption = None,
) -> None:
    """Remove rows with null values in specified columns or any column."""
    df = io_operations.read_dataframe(input_file)
    result = df.dropna(subset=get_columns(df, subset))
    io_operations.write_dataframe(result, get_output_options(use_json, fmt, output))
