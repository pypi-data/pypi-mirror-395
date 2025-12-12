#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to generate the resources_manifest.json file containing the file checksums for the resource files."""

import json
from pathlib import Path
from geogravl3.data_downloads.hashing import md5_file

script_dir = Path(__file__).resolve().parent
pkg_root = script_dir.parent  # geogravl3/
path_manifest_default = pkg_root / 'downloads' / 'resources_manifest.json'
path_resources = pkg_root / 'resources'


def build_manifest(path_out: Path | str = path_manifest_default):
    """
    Generate the resources_manifest.json file containing the file checksums for the resource files.

    Args:
        path_out (Path | str): output file path
    """
    files = {}

    for file_path in sorted(path_resources.rglob("*")):
        if file_path.is_file():
            rel = file_path.relative_to(path_resources).as_posix()
            checksum = md5_file(file_path)
            files[rel] = f"md5:{checksum}"

    manifest = {
        "_warning": "DO NOT EDIT MANUALLY, BUT RUN THE SCRIPT BELOW AFTER CHANGING RESOURCE FILES",
        "_generated_by": "python -m geogravl3.data_downloads.generate_resources_manifest",
        "base_url": "https://git.gfz-potsdam.de/grace_l3/geogravl3/-/raw/main/geogravl3/resources/",
        "files": files,
    }

    with open(path_out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to {path_out}, {len(files)} entries.")


if __name__ == "__main__":
    build_manifest()
