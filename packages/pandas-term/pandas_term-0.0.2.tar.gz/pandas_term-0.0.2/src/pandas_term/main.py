"""Main entry point for pandas-term."""

import typer

from pandas_term.cli import aggregate_commands, filter_commands, stats_commands, transform_commands

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})

app.add_typer(transform_commands.app)
app.add_typer(filter_commands.app)
app.add_typer(stats_commands.app)
app.add_typer(aggregate_commands.app)


if __name__ == "__main__":
    app()
