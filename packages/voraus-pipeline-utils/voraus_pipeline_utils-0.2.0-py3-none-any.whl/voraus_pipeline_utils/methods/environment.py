"""Contains all environment utils."""

import logging
import os
from typing import Any, Callable, Literal, overload

from voraus_pipeline_utils.constants import ENV_VAR_DOCKER_TAGS, ENV_VAR_IMAGE_NAME, ENV_VAR_REPOSITORIES

_logger = logging.getLogger(__file__)


def _get_env_or_none(env_var: str, decode: Callable[[str], Any] | None = None) -> Any:
    if (value := os.environ.get(env_var)) not in ["", None]:
        if decode is not None:
            result = decode(value)  # type: ignore
        else:
            result = value
    else:
        result = None
    return result


def is_jenkins() -> bool:
    """Tries to determine whether the current build is executed on a Jenkins or not.

    Returns:
        True if the current environment is on a Jenkins, False otherwise.
    """
    jenkins_url = _get_env_or_none("JENKINS_URL")
    _logger.debug(f"Jenkins URL is {jenkins_url}")
    return jenkins_url is not None


def get_git_tag() -> str | None:
    """Returns the TAG_NAME environment variable if set, else None.

    For a multibranch project corresponding to some kind of tag, this will be set to the name of the tag being built,
    if supported; else None.

    Returns:
        The git tag from the environment, else None.
    """
    tag = _get_env_or_none("TAG_NAME")
    _logger.debug(f"Tag is {tag}")
    return tag


def get_build_number() -> int | None:
    """Returns the build number if available.

    Returns:
        The build number if set or None.
    """
    build_number = _get_env_or_none("BUILD_NUMBER", decode=int)
    _logger.debug(f"Build number is {build_number}")
    return build_number


def get_branch_name() -> str | None:
    """Returns the branch name.

    Returns:
        The branch name if set or None.
    """
    branch_name = _get_env_or_none("BRANCH_NAME")
    _logger.debug(f"Branch name is {branch_name}")
    return branch_name


def get_change_target_branch_name() -> str | None:
    """Returns the branch name of the change target.

    Returns the `CHANGE_TARGET` environment variable. For a multibranch project corresponding to some kind of
    change request, this will be set to the target or base branch to which the change could be merged,
    if supported; else unset (None).

    Returns:
        The name of the branch the pull request points to if this is a pull request, None otherwise.
    """
    change_target = _get_env_or_none("CHANGE_TARGET")
    _logger.debug(f"Change target is {change_target}")
    return change_target


def get_docker_tags_from_env() -> list[str] | None:
    """Returns the docker tag list from an optional environment variable.

    Returns:
        The docker tag list from the environment variable ``ENV_VAR_DOCKER_TAGS`` if existing, else None.
    """
    docker_tags = _get_env_or_none(ENV_VAR_DOCKER_TAGS, lambda tag_str: tag_str.split(","))
    _logger.debug(f"Docker tags are {docker_tags}")
    return docker_tags


def get_docker_image_name_from_env() -> str | None:
    """Returns the docker image name from an optional environment variable.

    Returns:
        The docker image name from the environment variable ``ENV_VAR_IMAGE_NAME`` if existing, else None.
    """
    image_name = _get_env_or_none(ENV_VAR_IMAGE_NAME)
    _logger.debug(f"Docker image name is {image_name}")
    return image_name


@overload
def get_docker_repositories_from_env(raise_on_none: Literal[True]) -> list[str]: ...


@overload
def get_docker_repositories_from_env(raise_on_none: Literal[False]) -> list[str] | None: ...


def get_docker_repositories_from_env(raise_on_none: bool = False) -> list[str] | None:
    """Returns the docker repository list from an optional environment variable.

    Args:
        raise_on_none: If True, raises a ValueError if the environment variable is not set.

    Returns:
        The docker repository list from the environment variable ``ENV_VAR_REPOSITORIES`` if existing, else None.

    Raises:
        ValueError: If the environment variable is not set and ``raise_on_none`` is True.
    """
    repositories = _get_env_or_none(ENV_VAR_REPOSITORIES, lambda tag_str: tag_str.split(","))
    if not repositories and raise_on_none:
        raise ValueError(f"Unable to determine docker repositories from environment variable {ENV_VAR_REPOSITORIES}")
    _logger.debug(f"Docker repositories are {repositories}")
    return repositories
