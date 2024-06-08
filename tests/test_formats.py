"""Тестирование форматов"""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer.const import DEFAULT_FORMATS
from file_organizer.formats import read_config


class TestFormats:
    """Тестирование установки форматов для организации файлов"""

    formats = read_config()

    @pytest.mark.parametrize(
        "config_path,add_default,expected",
        [
            ("", False, DEFAULT_FORMATS),
            (Path("tests/configs/config.json"), False, {".test": Path("tests")}),
            (
                Path("tests/configs/config.json"),
                True,
                {
                    ".test": Path("tests"),
                    **DEFAULT_FORMATS,
                },
            ),
        ],
    )
    def test_read_config(
        self,
        config_path: Path,
        add_default: bool,
        expected: dict[str, Path],
    ) -> None:
        formats = read_config(
            config_path=config_path,
            add_default=add_default,
        )

        assert formats._formats == expected

    @pytest.mark.parametrize(
        "path,expected",
        [
            (Path("tests"), None),
            (Path("tests.py"), Path("unknown")),
            (Path("tests.txt"), Path("texts")),
        ],
    )
    def test_get_formats_dir(
        self,
        path: Path,
        expected: Path | None,
    ) -> None:
        if expected is None:
            assert self.formats.get_formats(path) is expected
            return

        assert self.formats.get_formats(path) == expected

    @pytest.mark.parametrize(
        "path,expected",
        [
            (Path("tes"), False),
            (Path("texts"), True),
        ],
    )
    def test_check_folder_format_not_found(
        self,
        path: Path,
        expected: bool,
    ) -> None:
        assert self.formats.check_folder_format(path) is expected
