"""CLI commands for dataframe aggregation operations."""

from typing import Annotated

import typer

from pandas_term.cli.options import InputFileArgument, OutputOption, UseJsonOption
from pandas_term.core import io_operations

app = typer.Typer(add_completion=False)


@app.command()
def value_counts(
    column: Annotated[str, typer.Argument(help="Column to count values in")],
    input_file: InputFileArgument = "-",
    normalize: Annotated[
        bool,
        typer.Option("--normalize", "-n", help="Return proportions instead of counts"),
    ] = False,
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Count unique values in a column."""
    df = io_operations.read_dataframe(input_file)
    result = df[column].value_counts(normalize=normalize).reset_index()
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def groupby(
    group_cols: Annotated[str, typer.Argument(help="Comma-separated list of columns to group by")],
    input_file: InputFileArgument = "-",
    col: Annotated[str | None, typer.Option("--col", "-c", help="Column to aggregate")] = None,
    agg: Annotated[
        str,
        typer.Option("--agg", "-a", help="Aggregation function (sum, mean, count, etc.)"),
    ] = "sum",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Group by columns and apply aggregation function."""
    if col is None:
        raise typer.BadParameter("--col is required")
    df = io_operations.read_dataframe(input_file)
    group_col_list = [c.strip() for c in group_cols.split(",")]
    result = df.groupby(group_col_list)[col].agg(agg).reset_index()
    io_operations.write_dataframe(result, output, use_json)
