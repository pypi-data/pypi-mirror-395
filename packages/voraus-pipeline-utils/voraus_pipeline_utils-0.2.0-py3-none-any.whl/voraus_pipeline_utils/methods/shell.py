"""Contains all shell helpers."""

import logging
import subprocess
from pathlib import Path
from typing import Callable

_logger = logging.getLogger(__name__)


def execute_command(
    command: list[str],
    stdout_fn: Callable | None = print,
    no_raise: bool = False,
    cwd: Path | None = None,
) -> tuple[int, list[str]]:
    """Executes the given command and returns the result.

    Args:
        command: The command to execute.
        stdout_fn: The function to write the output to. Defaults to print.
        no_raise: If True, no exception is raised if the command Fails. Defaults to False.
        cwd: The working directory. Defaults to None.

    Raises:
        ValueError: If the stdout property cannot be assigned to the process.
        subprocess.CalledProcessError: If the command fails and _raise is True.

    Returns:
        A tuple containing the exit code and the stdout as list of the command.
    """
    command_str = " ".join(command)
    _logger.debug(f"Executing command '{command_str}'")

    output: list[str] = []

    with subprocess.Popen(
        command_str,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Redirect stderr to stdout
        text=True,  # To get strings instead of bytes
        bufsize=1,  # Line-buffered
        shell=True,
        cwd=cwd,
    ) as process:
        if process.stdout is None:
            raise ValueError("Failed to set stdout for the subprocess.")

        for output_line in process.stdout:
            output_line = output_line.strip()
            output.append(output_line)
            if stdout_fn is not None:
                stdout_fn(output_line)

        # Wait for the process to complete
        process.wait()

        # Check the return code
        if process.returncode != 0 and not no_raise:
            raise subprocess.CalledProcessError(process.returncode, command)

    return process.returncode, output
