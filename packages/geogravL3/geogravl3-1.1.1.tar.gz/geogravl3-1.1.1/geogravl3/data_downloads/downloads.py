# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to download the files needed for geogravL3 which cannot be included in the package."""

import urllib.request
from logging import Logger
from pathlib import Path
import json
import logging
import os

from .hashing import md5_file
from ..utils.utils import get_resource_dir, create_test_logger


def download_resources(resources_dir: Path | str = None,
                       logger: Logger | None = None
                       ) -> Path:
    """Download resource files required for running geogravl3.

    NOTE: No download is done if we are running in local repository, then the local data is used
          (except if a custom resources_dir is provided).

    Args:
        resources_dir (Path | str):
            custom directory where to store the downloaded resource files (default: $HOME/.cache/geogravl3/resources)
        logger (Logger | None):
            logger to use for status messages

    Returns:
        Path: Path to the directory containing the resources.
    """
    if not logger:
        logger = create_test_logger()
        logger.setLevel(logging.INFO)

    if resources_dir and Path(resources_dir) != get_resource_dir():
        logger.info(f"Setting $GEOGRAVL3_DATA to the custom directory: {resources_dir}.")
        os.environ['$GEOGRAVL3_DATA'] = str(resources_dir)
        resources_dir = Path(resources_dir)
    else:
        resources_dir = get_resource_dir()

    # If we are in a local checkout → never download
    if (resources_dir / ".." / ".." / ".git").resolve().exists():
        logger.info("Using local repository resources; no download of resource files needed.")
        return resources_dir

    # Load manifest stored in the package
    manifest_path = Path(__file__).with_name("resources_manifest.json")
    manifest = json.loads(manifest_path.read_text())

    base_url = manifest["base_url"]
    files = manifest["files"]

    resources_dir.mkdir(parents=True, exist_ok=True)

    downloaded_count = 0

    for relpath, checksum in files.items():
        algo, expected_md5 = checksum.split(":")
        out_path = resources_dir / relpath
        out_path.parent.mkdir(parents=True, exist_ok=True)

        needs_download = (
            not out_path.exists()
            or md5_file(out_path) != expected_md5
        )

        if needs_download:
            if not downloaded_count:
                logger.info(f"Downloading geogravL3 resource files to {resources_dir}.")

            url = base_url + relpath
            logger.debug(f"Downloading {relpath} from {url}")

            success = False

            for attempt in range(3):
                try:
                    urllib.request.urlretrieve(url, out_path)
                except Exception:
                    continue

                if not out_path.exists():
                    continue

                if md5_file(out_path) == expected_md5:
                    success = True
                    downloaded_count += 1
                    break

            if not out_path.exists():
                logger.warning(f"File {relpath} does not exist after 3 download attempts.")
                raise FileNotFoundError(
                    f"Download of {relpath} failed after 3 attempts. "
                    f"Please download manually from {url} to {resources_dir}."
                )

            if not success:
                logger.warning(f"Checksum mismatch for {relpath} after 3 download attempts.")
                raise ValueError(
                    f"Downloaded file {relpath} is corrupted after 3 attempts. "
                    f"Please download manually from {url} to {resources_dir}. "
                    f"Otherwise, geogravL3 will fail at runtime."
                )

        else:
            logger.debug(f"{relpath} already present and valid.")

    if downloaded_count:
        logger.info(f"Downloaded {downloaded_count} file(s).")

    return resources_dir
