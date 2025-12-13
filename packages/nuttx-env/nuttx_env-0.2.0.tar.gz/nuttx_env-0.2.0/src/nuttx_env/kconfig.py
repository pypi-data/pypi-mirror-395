"""
Work with Kconfig files
kconfig-language.txt in the NuttX tools repository.

"""

from pathlib import Path

from . import vars


class KConfigUserBoard:
    """
    Class for working with user board Kconfig files
    """

    def __init__(self, kconfig_path: Path):
        self._kconfig_path = kconfig_path

    def get_user_board_config(self) -> list[str]:
        """
        Get user board config options from Kconfig file

        Return string with config options
        """
        return self._get_section_lines(
            start_marker="# ---- START USER BOARD CONFIG ----",
            end_marker="# ---- END USER BOARD CONFIG ----",
            insert_marker=True
        )

    def get_user_board_default(self) -> list[str]:
        """
        Get user board default options from Kconfig file

        Return string with default options
        """
        return self._get_section_lines(
            start_marker="# ---- START USER BOARD DEFAULT ----",
            end_marker="# ---- END USER BOARD DEFAULT ----",
            insert_marker=True
        )

    def get_user_board_options(self) -> list[str]:
        """
        Get user board options from Kconfig file

        Return string with board options
        """
        return self._get_section_lines(
            start_marker="# ---- START USER BOARD OPTIONS ----",
            end_marker="# ---- END USER BOARD OPTIONS ----",
            insert_marker=True
        )

    def get_section_place_user_board_config(self) -> tuple[int, int]:
        """
        Get start and end line numbers from user board config section

        Raise
            ValueError: if section not found

        Return tuple with start and end line numbers
        """
        return self._get_section_place(
            start_marker="# ---- START USER BOARD CONFIG ----",
            end_marker="# ---- END USER BOARD CONFIG ----",
        )

    def get_section_place_user_board_default(self) -> tuple[int, int]:
        """
        Get start and end line numbers from user board default section

        Raise
            ValueError: if section not found

        Return tuple with start and end line numbers
        """
        return self._get_section_place(
            start_marker="# ---- START USER BOARD DEFAULT ----",
            end_marker="# ---- END USER BOARD DEFAULT ----",
        )

    def get_section_place_user_board_options(self) -> tuple[int, int]:
        """
        Get start and end line numbers from user board options section

        Raise
            ValueError: if section not found

        Return tuple with start and end line numbers
        """
        return self._get_section_place(
            start_marker="# ---- START USER BOARD OPTIONS ----",
            end_marker="# ---- END USER BOARD OPTIONS ----",
        )

    def _check_kconfig_exists(self) -> None:
        """
        Check if Kconfig file exists

        Raise
            FileNotFoundError: if Kconfig file not found
        """
        if not self._kconfig_path.exists():
            raise FileNotFoundError(f"Kconfig file not found: {self._kconfig_path}")

    def _get_section_lines(
        self,
        start_marker: str,
        end_marker: str,
        insert_marker: bool = True
    ) -> list[str]:
        """
        Get lines from section between start and end markers

        Args:
            start_marker: Marker that indicates the start of the section
            end_marker: Marker that indicates the end of the section
            insert_marker: If True,
                include the start and end markers in the returned lines

        Return list of lines
        """
        self._check_kconfig_exists()

        in_section = False
        section_lines: list[str] = []

        with self._kconfig_path.open("r") as kconfig_file:
            for line in kconfig_file.readlines():
                if line.strip() == start_marker:
                    in_section = True
                    if insert_marker:
                        section_lines.append(line)
                    continue
                if line.strip() == end_marker:
                    in_section = False
                    if insert_marker:
                        section_lines.append(line)
                    break
                if in_section:
                    section_lines.append(line)

        return section_lines

    def _get_section_place(
        self,
        start_marker: str,
        end_marker: str,
    ) -> tuple[int, int]:
        """
        Get start and end line numbers from section
        between start and end markers

        Raise
            ValueError: if section not found

        Return tuple with start and end line numbers
        """
        self._check_kconfig_exists()

        in_section = False
        lineno_start: int | None = None
        lineno_end: int | None = None

        with self._kconfig_path.open("r") as kconfig_file:
            for idx, line in enumerate(kconfig_file.readlines()):
                if line.strip() == start_marker:
                    in_section = True
                    lineno_start = idx
                    continue
                if line.strip() == end_marker:
                    in_section = False
                    lineno_end = idx
                    break
                if in_section:
                    continue

        if lineno_start is None or lineno_end is None:
            raise ValueError("Section not found")

        return lineno_start, lineno_end


class KConfig:
    """
    Class for working with Kconfig files
    """

    def __init__(self, kconfig_path: Path):
        """
        Args:
            kconfig_path: Path to nuttx board Kconfig file
        """
        self._kconfig_path = kconfig_path

    def add_board(self) -> None:
        """
        Add board to Kconfig file

        Raise
            ValueError: if cannot find place to insert new board
        """
        user_board_kconfig = KConfigUserBoard(
            kconfig_path=vars.USER_BOARDS_DIR.joinpath("Kconfig"))
        nuttx_board_kconfig = KConfigUserBoard(
            kconfig_path=self._kconfig_path)

        lines = self._load()

        # Process config
        try:
            # Section exists
            s, e = nuttx_board_kconfig.get_section_place_user_board_config()
            self._replace_lines_at(
                lines=lines,
                replace_lines=user_board_kconfig.get_user_board_config(),
                lineno_start=s,
                lineno_end=e
            )
        except ValueError:
            # Section not found
            self._insert_lines_at(
                lines=lines,
                insert_lines=user_board_kconfig.get_user_board_config(),
                lineno=self._find_place_config_to_insert(lines)
            )

        # Process default
        try:
            # Section exists
            s, e = nuttx_board_kconfig.get_section_place_user_board_default()
            self._replace_lines_at(
                lines=lines,
                replace_lines=user_board_kconfig.get_user_board_default(),
                lineno_start=s,
                lineno_end=e
            )
        except ValueError:
            # Section not found
            self._insert_lines_at(
                lines=lines,
                insert_lines=user_board_kconfig.get_user_board_default(),
                lineno=self._find_place_default_to_insert(lines)
            )

        # Process options
        try:
            # Section exists
            s, e = nuttx_board_kconfig.get_section_place_user_board_options()
            self._replace_lines_at(
                lines=lines,
                replace_lines=user_board_kconfig.get_user_board_options(),
                lineno_start=s,
                lineno_end=e
            )
        except ValueError:
            # Section not found
            self._insert_lines_at(
                lines=lines,
                insert_lines=user_board_kconfig.get_user_board_options(),
                lineno=self._find_place_options_to_insert(lines)
            )

        # save Kconfig file
        with self._kconfig_path.open("w") as kconfig_file:
            kconfig_file.writelines(lines)

    def _load(self) -> list[str]:
        """
        Load Kconfig file, put lines to list and return it
        """
        with self._kconfig_path.open("r") as kconfig_file:
            return kconfig_file.readlines()

    def _find_place_config_to_insert(self, lines: list[str]) -> int:
        """
        Find first place to insert new board

        Raise
            ValueError: if place not found

        Return line number
        """
        return self._get_last_line_number_in_section(
            lines=lines,
            marker_start='choice',
            marker_end='endchoice'
        )

    def _find_place_default_to_insert(self, lines: list[str]) -> int:
        """
        Find first place to insert new board

        Raise
            ValueError: if place not found

        Return line number
        """
        return self._get_last_line_number_in_section(
            lines=lines,
            marker_start='config ARCH_BOARD',
            marker_end='comment "Common Board Options"'
        )

    def _find_place_options_to_insert(self, lines: list[str]) -> int:
        """
        Find second place to insert new board

        Raise
            ValueError: if place not found

        Return line number
        """
        return self._get_last_line_number_in_section(
            lines=lines,
            marker_start='comment "Board-Specific Options"',
            marker_end='comment "Board-Common Options"'
        )

    def _get_last_line_number_in_section(
        self,
        lines: list[str],
        marker_start: str,
        marker_end: str,
    ) -> int:
        """
        Get last line number in section between start and end markers

        Raise
            ValueError: if section not found

        Return line number
        """
        in_section = False
        lineno: int | None = None

        for idx, line in enumerate(lines):
            if line.strip() == marker_start:
                in_section = True
                continue
            if line.strip() == marker_end:
                in_section = False
                lineno = idx - 1
                break
            if in_section:
                continue

        if lineno is None:
            raise ValueError("Section not found")

        return lineno

    def _insert_lines_at(
        self,
        lines: list[str],
        insert_lines: list[str],
        lineno: int
    ):
        """
        Insert lines at specified line number

        Return modified lines list
        """
        lines[lineno:lineno] = insert_lines

    def _replace_lines_at(
        self,
        lines: list[str],
        replace_lines: list[str],
        lineno_start: int,
        lineno_end: int
    ):
        """
        Replace lines between specified line numbers

        Return modified lines list
        """
        lines[lineno_start:lineno_end + 1] = replace_lines
