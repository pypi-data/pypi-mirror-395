"""Contains all docker utils."""

from pathlib import Path

from voraus_pipeline_utils.methods.build import sanitize_branch_name
from voraus_pipeline_utils.methods.environment import (
    get_branch_name,
    get_build_number,
    get_docker_image_name_from_env,
    get_docker_repositories_from_env,
    get_docker_tags_from_env,
    get_git_tag,
    is_jenkins,
)
from voraus_pipeline_utils.methods.shell import execute_command


def get_tags_from_common_vars(
    tags: list[str] | None = None, repositories: list[str] | None = None, image_name: str | None = None
) -> list[str]:
    """Parses and returns the docker tags to use from the common environment variable.

    Args:
        tags: The docker tags provided by the CLI.
        repositories: The docker repositories provided by the CLI.
        image_name: The docker image name provided by the CLI.

    Returns:
        The list of docker image tags to use.
    """
    if tags is not None:
        return tags
    image_name = image_name or get_docker_image_name_from_env()
    repositories = repositories or get_docker_repositories_from_env(raise_on_none=True)
    tags = get_docker_tags_from_env() or get_all_docker_tags(image_name=image_name, repositories=repositories)

    return tags


def get_docker_image_tag(
    name: str,
    version_tag: str,
    target_repo: str = "docker",
    registry: str = "artifactory.vorausrobotik.com",
) -> str:
    """Constructs a valid docker tag from the given parameters.

    Args:
        name: The name of the image.
        version_tag: The version tag.
        target_repo: The target repository. Defaults to "docker".
        registry: The target registry. Defaults to "artifactory.vorausrobotik.com".

    Returns:
        The docker image tag.
    """
    return f"{registry}/{target_repo}/{name}:{version_tag}"


def get_all_docker_tags(
    image_name: str | None,
    repositories: list[str],
    branch_name: str | None = None,
    build_number: int | None = None,
    tag: str | None = None,
) -> list[str]:
    """Returns a list of all docker tags for the given values / environment.

    Args:
        image_name: The docker image name.
        repositories: A list of all repositories to publish to.
        branch_name: The branch name. Defaults to None.
        build_number: The build number. Defaults to None.
        tag: The build tag. Defaults to None.

    Raises:
        ValueError: If an invalid combination of input parameters are provided.

    Returns:
        A list of docker images for the given values / environment.
    """
    if len(repositories) == 0:
        raise ValueError("No repositories provided")
    branch_name = branch_name or get_branch_name()
    build_number = build_number or get_build_number()
    tag = tag or get_git_tag()
    version_tags: list[str] = []
    docker_tags: list[str] = []
    if image_name in ["", None]:
        raise ValueError("Invalid image name")
    if branch_name and build_number is None:
        raise ValueError("Build number must be provided when branch name is given")
    if tag:
        version_tags.append(tag)
        version_tags.append("latest")
    elif branch_name:
        sanitized_branch_name = sanitize_branch_name(branch_name=branch_name)
        version_tags.append(f"{sanitized_branch_name}-latest")
        version_tags.append(f"{sanitized_branch_name}-{build_number}")
    else:  # pragma: no cover
        raise ValueError(f"Invalid combination of branch_name={branch_name}, build_number={build_number} and tag={tag}")

    for version_tag in version_tags:
        for repository in repositories:
            docker_tags.append(
                get_docker_image_tag(
                    name=image_name,  # type:ignore [arg-type]  # The image_name can't be None here
                    version_tag=version_tag,
                    target_repo=repository,
                )
            )

    return docker_tags


def docker_build_wrapper(
    *,
    dockerfile: Path = Path("Dockerfile"),
    path: Path = Path("."),
    tags: list[str] | None = None,
    pull: bool = True,
    use_jfrog: bool | None = None,
    build_args: dict[str, str] | None = None,
) -> None:
    """Wrapper for docker build. Optionally uses the JFrog CLI.

    Args:
        dockerfile: The path to the Dockerfile to use. Defaults to Path("Dockerfile").
        path: The build path. Defaults to Path(".").
        tags: The tags for the docker image. Defaults to None.
        pull: Whether to pull the base image. Defaults to True.
        use_jfrog: If True, the JFrog CLI will be used as additional wrapper.
            If executed on Jenkins, this defaults to True.
        build_args: Additional build arguments for docker.

    """
    build_args = build_args or {}
    tags = tags or []
    use_jfrog = use_jfrog if use_jfrog is not None else is_jenkins()
    execute_command(
        command=[
            *(["jf"] if use_jfrog else []),
            "docker",
            "build",
            *(["--pull"] if pull else []),
            *[f"-t {tag}" for tag in tags],
            *[f"--build-arg {key}={value}" for key, value in build_args.items()],
            "-f",
            str(dockerfile),
            str(path),
        ]
    )


def docker_push_wrapper(
    tags: list[str],
    use_jfrog: bool | None = None,
) -> None:
    """Wrapper for docker push. Optionally uses the JFrog CLI.

    Args:
        tags: The tags to push.
        use_jfrog: If True, the JFrog CLI will be used as additional wrapper.
            If executed on Jenkins, this defaults to True.

    """
    use_jfrog = use_jfrog if use_jfrog is not None else is_jenkins()
    for tag in tags:
        execute_command(command=[*(["jf"] if use_jfrog else []), "docker", "push", tag])
