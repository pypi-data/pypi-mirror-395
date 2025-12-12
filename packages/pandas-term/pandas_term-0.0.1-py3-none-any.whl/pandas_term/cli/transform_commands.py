"""CLI commands for dataframe transformations."""

from typing import Annotated, Literal

import pandas as pd
import typer

from pandas_term.cli.options import InputFileArgument, OutputOption, UseJsonOption
from pandas_term.core import io_operations, transforms, validation

app = typer.Typer(add_completion=False)


@app.command()
def select(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to select")],
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Select provided columns from the dataframe."""
    df = io_operations.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    validation.validate_columns(df, column_list)
    result = df[column_list]
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def drop(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to drop")],
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Drop provided columns from the dataframe."""
    df = io_operations.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    validation.validate_columns(df, column_list)
    result = df.drop(columns=column_list)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def sort(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to sort by")],
    input_file: InputFileArgument = "-",
    ascending: Annotated[bool, typer.Option("--ascending/--descending", help="Sort order")] = True,
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Sort dataframe by specified columns."""
    df = io_operations.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    result = df.sort_values(by=column_list, ascending=ascending)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def rename(
    mapping: Annotated[str, typer.Argument(help="Rename mapping as 'old:new,old2:new2'")],
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Rename columns in the dataframe."""
    df = io_operations.read_dataframe(input_file)
    rename_map = {}
    for pair in mapping.split(","):
        old, new = pair.strip().split(":")
        rename_map[old.strip()] = new.strip()
    result = df.rename(columns=rename_map)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def dedup(
    input_file: InputFileArgument = "-",
    subset: Annotated[
        str | None,
        typer.Option(
            "--subset", "-s", help="Comma-separated list of columns to consider for duplicates"
        ),
    ] = None,
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Remove duplicate rows from the dataframe."""
    df = io_operations.read_dataframe(input_file)
    subset_list = [col.strip() for col in subset.split(",")] if subset else None
    result = df.drop_duplicates(subset=subset_list)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def merge(
    left_file: Annotated[str, typer.Argument(help="Left dataframe file path")],
    right_file: Annotated[str, typer.Argument(help="Right dataframe file path")],
    on: Annotated[
        str | None,
        typer.Option("--on", help="Comma-separated list of columns to merge on"),
    ] = None,
    how: Annotated[
        Literal["inner", "left", "right", "outer", "cross"],
        typer.Option("--how", help="Type of merge: inner, left, right, outer, cross"),
    ] = "inner",
    left_on: Annotated[
        str | None,
        typer.Option("--left-on", help="Left dataframe column to merge on"),
    ] = None,
    right_on: Annotated[
        str | None,
        typer.Option("--right-on", help="Right dataframe column to merge on"),
    ] = None,
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Merge two dataframes."""
    left_df = io_operations.read_dataframe(left_file)
    right_df = io_operations.read_dataframe(right_file)
    on_list = [col.strip() for col in on.split(",")] if on else None
    result = left_df.merge(right_df, on=on_list, how=how, left_on=left_on, right_on=right_on)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def concat(
    files: Annotated[list[str], typer.Argument(help="Files to concatenate")],
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Concatenate multiple dataframes vertically."""
    dfs = [io_operations.read_dataframe(f) for f in files]
    result = pd.concat(dfs, ignore_index=True)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def batch(
    input_file: InputFileArgument = "-",
    sizes: Annotated[
        str,
        typer.Option("--sizes", "-s", help="Comma-separated batch sizes (last size repeats)"),
    ] = "100",
    output_pattern: Annotated[
        str,
        typer.Option("--output", "-o", help="Output file pattern (e.g., 'batch_{}.csv')"),
    ] = "batch_{}.csv",
) -> None:
    """Split dataframe into batches and write to separate files."""
    df = io_operations.read_dataframe(input_file)
    size_list = [int(s.strip()) for s in sizes.split(",")]
    batches = transforms.batch_dataframe(df, size_list)

    for i, batch_df in enumerate(batches):
        output_file = output_pattern.format(i)
        io_operations.write_dataframe(batch_df, output_file)
        typer.echo(f"Written batch {i} to {output_file} ({len(batch_df)} rows)")
