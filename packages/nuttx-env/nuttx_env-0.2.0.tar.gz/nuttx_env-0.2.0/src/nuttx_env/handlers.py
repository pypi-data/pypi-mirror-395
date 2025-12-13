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
from .kconfig import KConfig


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


def board_find_by_name(name: str, boards_path: Path) -> Path | None:
    """
    Find board by name in src/my-boards/<arh>/<chip>/<board name>
    Return path to board or None if not found
    """
    if not boards_path.exists():
        return None

    for arh_dir in boards_path.iterdir():
        if not arh_dir.is_dir():
            continue
        for chip_dir in arh_dir.iterdir():
            if not chip_dir.is_dir():
                continue
            for board_dir in chip_dir.iterdir():
                if not board_dir.is_dir():
                    continue
                if board_dir.name == name:
                    return board_dir

    return None


def board_get_arh_chip_from_path(board_path: Path) -> str | None:
    """
    Get architecture/chip from board path
    Place board not important
    Return  string<arh>/<chip> or None if not found
    """
    try:
        parts = board_path.resolve().parts
        if len(parts) < 3:
            return None
        arh, chip = parts[-3], parts[-2]
        return f"{arh}/{chip}"
    except ValueError:
        return None


def board_add_to_kconfig(board_name: str):
    """
    Add board to Kconfig

    Raises
        ValueError
    """
    # Get path to board
    board_path = board_find_by_name(
        board_name,
        boards_path=Path("src/nuttx/boards")
    )
    if board_path is None:
        raise ValueError(f"Board '{board_name}' not found")
    # get chip/arch
    arh_chip = board_get_arh_chip_from_path(board_path)
    if arh_chip is None:
        raise ValueError(
            "Cannot determine architecture/chip from board path")

    # Find
    kconfig = KConfig(Path("src/nuttx/boards/Kconfig"))
    kconfig.add_board(board_name, arh_chip)


# --- Handlers ---

def handle_init(args: argparse.Namespace):
    """
    Handle init command - create empty NuttX environment
    """
    # TODO: Add check on exists project

    # Get nuttx version
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
            "src/.gitignore",
            (
                "nuttx/*\n"
                "apps/*\n"
            )
        ),
        (
            "src/my-boards/Kconfig",
            (
                "# Kconfig for my-boards\n"
                "\n"
                "choice\n"
                "\tprompt \"Select target board\"\n"
                "\tdefault ARCH_BOARD_CUSTOM\n"
                "\n"
                "# ---- START USER BOARD CONFIG ----\n"
                "# Add your board configs here\n"
                "# ---- END USER BOARD CONFIG ----\n"
                "\n"
                "endchoice\n"
                "\n"

                "config ARCH_BOARD\n"
                "\tstring\n"
                "\n"
                "# ---- START USER BOARD DEFAULT ----\n"
                "# Set your default board here\n"
                "# ---- END USER BOARD DEFAULT ----\n"
                "\n"

                "comment \"Board-Specific Options\"\n"
                "\n"
                "# ---- START USER BOARD OPTIONS ----\n"
                "# Add your board-specific options here\n"
                "# ---- END USER BOARD OPTIONS ----\n"
            )
        )
    ]
    for directory in directories:
        dir_path = os.path.join(current_dir, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

    for item in files:
        file_name, content = item
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            print(f"File already exists: {file_name}, skipping")
            continue
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


def handler_board(args: argparse.Namespace):
    """
    Handler board command
    """
    if args.subcommand == "add":
        """
        Add board to NuttX environment
        """
        if args.name is None:
            raise ValueError("Board name is required for add subcommand")
        board_path = board_find_by_name(
            args.name, boards_path=vars.USER_BOARDS_DIR)
        if board_path is None:
            raise ValueError(f"Board '{args.name}' not exists")

        # Process adding board
        arh_chip = board_get_arh_chip_from_path(board_path)
        if arh_chip is None:
            raise ValueError(
                "Cannot determine architecture/chip from board path")
        # Check target arh/chip directory
        target_board_dir = vars.NUTTX_BOARDS_DIR.joinpath(arh_chip)
        if not target_board_dir.exists():
            raise ValueError(
                f"Architecture/chip directory not found: {target_board_dir}")

        # Create link on board in src/nuttx/boards/<arh>/<chip>/<board name>
        link_path = target_board_dir.joinpath(args.name)
        if link_path.exists():
            print(f"Board link already exists: {link_path}")
        else:
            os.symlink(
                os.path.relpath(board_path, start=target_board_dir),
                link_path,
                target_is_directory=True
            )
            print(f"Created board link: {link_path} -> {board_path}")

        # Add all board Kconfig to nuttx/boards/Kconfig
        KConfig(
            kconfig_path=vars.NUTTX_BOARDS_DIR.joinpath("Kconfig")
        ).add_board()

        print(f"Board '{args.name}' added successfully")

    elif args.subcommand == "remove":
        print("Not implemented yet")
    elif args.subcommand == "list":
        """
        Handle board list subcommand
        Search boards in src/my-boards
        and apply filter <arh>/<chip>/<board name>
        """
        boards_path = Path("src/my-boards")
        if not boards_path.exists():
            print("Boards directory not found")
            return

        board_dirs: list[Path] = []
        for arh_dir in boards_path.iterdir():
            if not arh_dir.is_dir():
                continue
            for chip_dir in arh_dir.iterdir():
                if not chip_dir.is_dir():
                    continue
                for board_dir in chip_dir.iterdir():
                    if not board_dir.is_dir():
                        continue
                    board_dirs.append(board_dir)

        if not board_dirs:
            print("No boards found")
            return

        print("Boards:")
        for board_dir in board_dirs:
            print(" ", board_dir.name)
    else:
        # Should not happen
        raise ValueError("Unknown subcommand")
