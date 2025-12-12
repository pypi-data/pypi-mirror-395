#!/bin/env python3
"""Identify and list files that override upstream templates and such."""

import os
import pathlib
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from importlib.metadata import files as package_files
from typing import Iterable

import invenio_theme_tuw


def similarity_ratio(a: str, b: str) -> float:
    """Calculate the similarity ratio between the two strings."""
    return SequenceMatcher(a=a, b=b).ratio()


@dataclass
class FileOverride:
    """Information about an overriding file and its base."""

    file_path: pathlib.Path
    base: str
    base_package: str
    base_version: str | None

    def _find_possible_base_files(self) -> Iterable[pathlib.Path]:
        """Collect a list of base file candidates, ordered by path similarity."""
        matches = []

        # if the base was specified as more than just a package name (i.e. a file
        # or import path), we use that to search for the base files
        search_file = self.base if self.base != self.base_package else None
        for file_ in package_files(self.base_package):
            file_path = file_.locate()
            if search_file is not None:
                if search_file in file_path:
                    matches.append(file_path)
            else:
                if file_path.name == self.file_path.name:
                    matches.append(file_path)

        # sort the matches by their similarity to the search file's name if given,
        # or by the override file's name
        ofp = search_file or str(self.file_path)
        matches.sort(key=lambda fp: similarity_ratio(ofp, str(fp)), reverse=True)

        return matches

    @property
    def base_file_path(self) -> pathlib.Path | None:
        """Get the path for the (most likely) base file."""
        matches = self._find_possible_base_files()
        return matches[0] if matches else None


# e.g. "{#- base: invenio-app-rdm v13.0.0 -#}"
# or "// base: invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm/header.html"
marker_pattern = re.compile(r"base:\s+([0-9A-Za-z/._-]+)\s*v?([0-9.]+)?")


def find_overrides(base_path: str) -> Iterable[FileOverride]:
    """Collect information about files that override upstream files."""
    files_list = [
        f"{root}/{file}" for root, _, files in os.walk(base_path) for file in files
    ]
    file_overrides = []
    for file_name in files_list:
        file_path = package_path / file_name
        with open(file_path, "r") as open_file:
            try:
                if result := marker_pattern.search(open_file.read()):
                    # we allow the base to be specified as either file or import path
                    base = result.group(1)
                    base_package = base.split("/")[0].split(".")[0]
                    base_version = result.group(2)
                    file_overrides.append(
                        FileOverride(file_path, base, base_package, base_version)
                    )

            except UnicodeDecodeError:
                # we're not interested in binary files (e.g. pyc)
                pass

    return file_overrides


if __name__ == "__main__":
    package_path = pathlib.Path(invenio_theme_tuw.__file__).parent
    file_overrides = find_overrides(package_path)
    for override in file_overrides:
        print(f"{override.file_path}:{override.base_file_path}")
