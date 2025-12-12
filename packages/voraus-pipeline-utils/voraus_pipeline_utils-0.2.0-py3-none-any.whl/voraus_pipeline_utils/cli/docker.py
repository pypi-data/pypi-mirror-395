"""This module defines the typer docker wrapper."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from voraus_pipeline_utils.methods.docker import docker_build_wrapper, docker_push_wrapper, get_tags_from_common_vars

app = typer.Typer(name="docker")


@app.command("build", help="Wrapper for docker build that optionally uses JFrog CLI and auto generates image tags")
def _cli_docker_build(
    image_name: Annotated[
        Optional[str],
        typer.Option(help="Docker image name. Ignored, if tag(s) are provided."),
    ] = None,
    tag: Annotated[
        Optional[list[str]],
        typer.Option(help="Docker image tag(s)"),
    ] = None,
    repository: Annotated[
        Optional[list[str]],
        typer.Option(help="Docker repository or repositories"),
    ] = None,
    dockerfile: Annotated[
        Path,
        typer.Option("--file", "-f", help="Dockerfile to use for building the image"),
    ] = Path("Dockerfile"),
) -> None:  # noqa: disable=D103
    tags = get_tags_from_common_vars(tags=tag, repositories=repository, image_name=image_name)
    docker_build_wrapper(tags=tags, dockerfile=dockerfile)


@app.command("push", help="Wrapper for docker push that optionally uses JFrog CLI and auto uses generated image tags")
def _cli_docker_push(
    image_name: Annotated[
        Optional[str],
        typer.Option(help="Docker image name. Ignored, if tag(s) are provided."),
    ] = None,
    tag: Annotated[
        Optional[list[str]],
        typer.Option(help="Docker image tag(s)"),
    ] = None,
    repository: Annotated[
        Optional[list[str]],
        typer.Option(help="Docker repository or repositories"),
    ] = None,
) -> None:  # noqa: disable=D103
    tags = get_tags_from_common_vars(tags=tag, repositories=repository, image_name=image_name)
    docker_push_wrapper(tags=tags)
