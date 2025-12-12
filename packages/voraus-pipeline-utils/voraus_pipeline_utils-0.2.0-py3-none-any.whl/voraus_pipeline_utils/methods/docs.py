"""Contains all docs utils."""

import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import requests


def docs_upload_wrapper(
    *,
    build_dir: Path,
    api_url: str,
    project_name: str,
    project_version: str,
    api_user: str,
    api_token: str,
) -> None:
    """Uploads documentation to a docs (vdoc) instance.

    Args:
        build_dir: The directory containing the HTML documentation to upload.
        project_name: The name of the project to upload documentation to.
        project_version: The version of the project to upload documentation to.
        api_user: The API user for the docs instance.
        api_url: The URL of the docs instance to upload documentation to.
        api_token: The API token for the docs instance.

    Raises:
        FileNotFoundError: If the index.html file is not found in the build directory.

    """
    if not (build_dir / "index.html").is_file():
        raise FileNotFoundError(f"Index file not found in {build_dir}")

    with TemporaryDirectory() as tmp_dir:
        zip_file_path = Path(tmp_dir) / "docs.zip"
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_handler:
            for file in build_dir.rglob("*"):
                zip_handler.write(file, arcname=file.relative_to(build_dir))

        response = requests.post(
            f"{api_url.rstrip('/')}/projects/{project_name}/versions/{project_version}",
            auth=(api_user, api_token),
            files={"file": (zip_file_path.name, zip_file_path.read_bytes(), "application/zip")},
            timeout=60,
        )
        response.raise_for_status()
