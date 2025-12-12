"""Contains the main CLI entry point."""

import logging

import typer
from voraus_logging_lib.logging import LogLevel, configure_logger

from voraus_pipeline_utils import get_app_name, get_app_version
from voraus_pipeline_utils.cli.docker import app as DOCKER_TYPER
from voraus_pipeline_utils.cli.docs import app as DOCS_TYPER

_logger = logging.getLogger(__name__)


app = typer.Typer()

app.add_typer(DOCKER_TYPER)
app.add_typer(DOCS_TYPER)


def print_version(do_print: bool) -> None:
    """Prints the version of the software.

    Args:
        do_print: If the version shall be printed.

    Raises:
        typer.Exit: After the version was printed.
    """
    if do_print:
        print(get_app_version())
        raise typer.Exit()


@app.callback()
def _common(
    _: bool = typer.Option(
        False,
        "--version",
        callback=print_version,
        is_eager=True,
        help="Print the installed version of the software.",
    ),
    log_level: LogLevel = typer.Option(LogLevel.INFO, help="The log level"),
) -> None:
    configure_logger(log_level=log_level.value)
    _logger.info(f"Using {get_app_name()}@v{get_app_version()}")


typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":  # pragma: no cover
    app()
