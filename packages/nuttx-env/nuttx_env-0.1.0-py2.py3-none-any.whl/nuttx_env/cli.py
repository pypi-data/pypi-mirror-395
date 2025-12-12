import argparse
import re
import sys
from enum import StrEnum
from typing import Callable

from . import handlers
from . import vars


class Commands(StrEnum):
    INIT = "init"
    INFO = "info"


def regex_type_wrap(pat: re.Pattern) -> Callable[[str], str]:
    def wrap(arg_value: str):
        if not pat.match(arg_value.strip()):
            raise argparse.ArgumentTypeError(f"Invalid value: {arg_value}")
        return arg_value
    return wrap


def args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Return arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "A Python library for creating and managing "
            "project environments for RTOS NuttX."
        )
    )
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        help="Available commands",
        required=True,
    )

    # --- Command: init ---
    cmd_init = subparsers.add_parser(
        Commands.INIT.value,
        help="Initialize empty NuttX environment in current folder"
    )
    cmd_init.add_argument(
        "--version",
        help="NuttX version",
        type=regex_type_wrap(vars.pattern_nuttx_version),
        default=vars.NUTTX_VERSION_LATEST
    )

    # --- Command: info ---
    cmd_info = subparsers.add_parser(
        Commands.INFO.value,
        help="Show information about avaliable Nuttx"
    )
    # help="Show information about current NuttX environment"

    return parser.parse_args(args)


def main():
    """
    Main entry point for 'nuttx-env'
    """
    handlers_map: dict[Commands, Callable] = {
        Commands.INIT: handlers.handle_init,
        Commands.INFO: handlers.handler_info,
    }
    parsed_args = args()

    try:
        handlers_map.get(Commands(parsed_args.command))(
            args=parsed_args
        )
    except (KeyError, ValueError):
        print("No command specified. Use --help for available commands.")
        sys.exit(1)
