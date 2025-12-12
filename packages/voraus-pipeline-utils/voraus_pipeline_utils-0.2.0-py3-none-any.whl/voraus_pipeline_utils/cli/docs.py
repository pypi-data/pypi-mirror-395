"""This module defines the typer docs wrapper."""

from pathlib import Path
from typing import Annotated

import typer

from voraus_pipeline_utils.methods.docs import docs_upload_wrapper

app = typer.Typer(name="docs")


@app.command("upload", help="Uploads HTML documentation to a vdoc instance")
def _cli_docs_upload(
    *,
    build_dir: Annotated[
        Path,
        typer.Argument(
            help="Path to the directory containing the HTML documentation to upload.",
        ),
    ] = Path("docs/build/html"),
    project_name: Annotated[
        str,
        typer.Option(help="Name of the vdoc project to upload documentation to.", envvar="PROJECT_NAME"),
    ],
    project_version: Annotated[
        str,
        typer.Option(help="Version of the vdoc project to upload documentation to.", envvar="PROJECT_VERSION"),
    ],
    api_url: Annotated[
        str,
        typer.Option(help="API URL of the vdoc instance to upload documentation to.", envvar="API_URL"),
    ] = "https://docs.vorausrobotik.com/api",
    api_user: Annotated[
        str,
        typer.Option(help="API user for the vdoc instance.", envvar="API_USER"),
    ],
    api_token: Annotated[
        str,
        typer.Option(help="API token for the vdoc instance.", envvar="API_TOKEN"),
    ],
) -> None:  # noqa: disable=D103
    docs_upload_wrapper(
        build_dir=build_dir,
        api_url=api_url,
        api_user=api_user,
        api_token=api_token,
        project_name=project_name,
        project_version=project_version,
    )
