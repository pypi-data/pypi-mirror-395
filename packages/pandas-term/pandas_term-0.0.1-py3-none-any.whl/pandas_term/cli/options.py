"""Shared CLI options for all commands."""

from typing import Annotated

import typer

InputFileArgument = Annotated[
    str,
    typer.Argument(help="Input file path (default: stdin)"),
]

UseJsonOption = Annotated[
    bool,
    typer.Option("--json", "-j", help="Output as JSON instead of CSV"),
]

OutputOption = Annotated[
    str | None,
    typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
]
