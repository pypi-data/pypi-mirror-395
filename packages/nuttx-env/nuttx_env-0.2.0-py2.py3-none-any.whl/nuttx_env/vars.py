"""
Stored vars
"""
import re
from pathlib import Path


# --- Common ---

NUTTX_GITHUB_REPO: str = "https://github.com/apache/nuttx"
NUTTX_APPS_GITHUB_REPO: str = "https://github.com/apache/nuttx-apps"

# Patterns
NUTTX_VERSION_LATEST = "latest"
REGEX_NUTTX_VERSION = r"(?P<version>\d+\.\d+\.\d+)"
REGEX_NUTTX_RC = r"(?P<rc>RC\d+)"

# Version pattern, rc options
pattern_nuttx_version = re.compile(
    rf"^({REGEX_NUTTX_VERSION}(?:-{REGEX_NUTTX_RC})?)|{NUTTX_VERSION_LATEST}$"
)
# Tags format. Examples: nuttx-12.3.0; nuttx-12.3.0-RC0
pattern_nuttx_tag = re.compile(
    rf"^nuttx-{REGEX_NUTTX_VERSION}(?:-{REGEX_NUTTX_RC})?$"
)


# --- Application ---

NUTTX_ARCHIV_NAME = "nuttx-{version}.zip"
NUTTX_APPS_ARCHIV_NAME = "nuttx-apps-{version}.zip"


# --- Paths ---
# The all path are relative to the project root directory

# Where user boards are stored
USER_BOARDS_DIR = Path("src/my-boards")

# NuttX source directories
NUTTX_DIR = Path("src/nuttx")
NUTTX_APPS_DIR = Path("src/apps")
NUTTX_BOARDS_DIR = NUTTX_DIR.joinpath("boards")
