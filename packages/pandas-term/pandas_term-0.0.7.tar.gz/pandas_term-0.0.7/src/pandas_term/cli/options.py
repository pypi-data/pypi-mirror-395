"""Shared CLI options for all commands."""

from dataclasses import dataclass
from typing import Annotated, Literal

import typer

OutputFormat = Literal["csv", "json", "tsv", "md", "markdown"]


@dataclass
class OutputOptions:
    """Options for outputting dataframes."""

    file: str | None = None
    format: OutputFormat = "csv"


InputFileArgument = Annotated[
    str,
    typer.Argument(help="Input file path (default: stdin)"),
]

UseJsonOption = Annotated[
    bool,
    typer.Option("--json", "-j", help="Output as JSON (shorthand for --format json)"),
]

FormatOption = Annotated[
    OutputFormat | None,
    typer.Option("--format", "-f", help="Output format: csv, json, tsv, md"),
]

OutputFileOption = Annotated[
    str | None,
    typer.Option("--output", "-o", help="Output file path (default: stdout)"),
]


def get_output_options(
    use_json: bool = False,
    fmt: OutputFormat | None = None,
    output: str | None = None,
) -> OutputOptions:
    """Build OutputOptions from command arguments."""
    if use_json and fmt is not None:
        raise typer.BadParameter("Cannot specify both --json and --format")

    if use_json:
        resolved_format: OutputFormat = "json"
    elif fmt == "markdown":
        resolved_format = "md"
    elif fmt is not None:
        resolved_format = fmt
    else:
        resolved_format = "csv"

    return OutputOptions(file=output, format=resolved_format)
