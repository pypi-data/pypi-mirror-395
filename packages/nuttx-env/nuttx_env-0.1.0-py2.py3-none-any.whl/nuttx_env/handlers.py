"""
Handlers
"""
from __future__ import annotations

import os
import zipfile
import argparse
from pathlib import Path
from dataclasses import dataclass

import platformdirs

from . import github as gh
from . import vars
from . import __app_name__
from . import utils


@dataclass
class NuttxVersion():
    version: str
    rc: str | None = None

    @staticmethod
    def from_github_tag(tag: str) -> "NuttxVersion":
        """
        Create from github tag

        Raises
            ValueError
        """
        m = vars.pattern_nuttx_tag.match(tag)
        if m is None:
            raise ValueError("Wrong tag format")
        return NuttxVersion(version=m.group("version"), rc=m.group("rc"))

    @staticmethod
    def from_version(version: str) -> "NuttxVersion":
        """
        Create from version string
        """
        m = vars.pattern_nuttx_version.match(version)
        if m is None or m.group("version") == vars.NUTTX_VERSION_LATEST:
            raise ValueError("Wrong version format")
        return NuttxVersion(version=m.group("version"), rc=m.group("rc"))

    def to_tag(self) -> str:
        """
        Return version in format nuttx tag repository
        """
        rc = ""
        if self.rc:
            rc = f"-{self.rc}"
        return f"nuttx-{self.version}{rc}"

    def __str__(self):
        rc = ""
        if self.rc:
            rc = f"-{self.rc}"
        return f"{self.version}{rc}"


# --- Methods ---

def gh_nuttx_get_tags() -> list[gh.GitHubTag]:
    """
    Retrun all tags from NuttX repository
    Order from newest to oldest
    """
    return gh.get_github_tags(*gh.gh_parse_url(vars.NUTTX_GITHUB_REPO))


def unzip_flat(zip_path: Path, extract_to: Path):
    """
    Extract zip archiv without first directory
    """
    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            # remove first segment path (root directory)
            parts = Path(member.filename).parts
            relative = Path(*parts[1:])

            if not relative:
                continue  # skip root dir

            target = extract_to / relative

            # Extract dir or file
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())

            # --- Restore permissions ---
            # upper 16 bits contain UNIX mode
            perm = member.external_attr >> 16
            if perm != 0:
                try:
                    os.chmod(target, perm)
                except FileNotFoundError:
                    pass  # should not happen


# --- Handlers ---

def handle_init(args: argparse.Namespace):
    """
    Handle init command - create empty NuttX environment
    """
    # TODO: Add check on exists project

    # Get version
    if args.version == vars.NUTTX_VERSION_LATEST:
        version = NuttxVersion.from_github_tag(gh_nuttx_get_tags()[0].name)
    else:
        version = NuttxVersion.from_version(args.version)

    # Check archiv nuttx
    nuttx_cache_path = platformdirs.user_cache_path(
        appname=__app_name__, ensure_exists=True
    ).joinpath(
        vars.NUTTX_ARCHIV_NAME.format(version=version)
    )
    if not nuttx_cache_path.exists():
        print(f"Start downloading: {nuttx_cache_path.name}")
        utils.downloader(
            gh.gh_download_repo(
                repo_url=vars.NUTTX_GITHUB_REPO,
                tag=version.to_tag()
            ),
            out=nuttx_cache_path
        )
    else:
        print(f"Using cached NuttX {version}")

    # Check archiv nuttx-apps
    nuttx_apps_cache_path = platformdirs.user_cache_path(
        appname=__app_name__, ensure_exists=True
    ).joinpath(
        vars.NUTTX_APPS_ARCHIV_NAME.format(version=version)
    )
    if not nuttx_apps_cache_path.exists():
        print(f"Start downloading: {nuttx_apps_cache_path.name}")
        utils.downloader(
            gh.gh_download_repo(
                repo_url=vars.NUTTX_APPS_GITHUB_REPO,
                tag=version.to_tag()
            ),
            out=nuttx_apps_cache_path
        )
    else:
        print(f"Using cached NuttX Apps {version}")

    # Directory structure
    current_dir = os.getcwd()
    directories = [
        "src",
        "src/my-boards",
        "src/my-apps",
    ]
    files = [
        ("README.md", ""),
        (
            ".gitignore",
            (
                "src/nuttx/*\n"
                "src/apps/*\n"
            )
        )
    ]
    for directory in directories:
        dir_path = os.path.join(current_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {directory}")

    for item in files:
        file_name, content = item
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created file: {file_name}")

    # Extract nuttx
    print(f"Start extracting: {nuttx_cache_path.name}")
    unzip_flat(nuttx_cache_path, Path("src/nuttx"))

    # Extract nuttx apps
    print(f"Start extracting: {nuttx_apps_cache_path.name}")
    unzip_flat(nuttx_apps_cache_path, Path("src/apps"))


def handler_info(args: argparse.Namespace):
    """
    Handler info command
    """
    # Convert tag to version.
    versions = [
        NuttxVersion.from_github_tag(item.name) for item in gh_nuttx_get_tags()
    ]

    # View
    print("NuttX versions:")
    for ver in versions:
        if ver.rc is not None:
            continue
        print(" ", ver.version)
