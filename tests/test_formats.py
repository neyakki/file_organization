"""Тестирование форматов"""

from __future__ import annotations

from pathlib import Path

from file_organizer.const import DEFAULT_FORMATS
from file_organizer.formats import read_config


class TestFormats:
    """Тестирование установки форматов для организации файлов"""
    formats = read_config()

    def test_read_config_default(self) -> None:
        formats = read_config()

        assert formats._formats == DEFAULT_FORMATS

    def test_read_config_without_default(self) -> None:
        formats = read_config(
            config_path=Path("tests/configs/config.json"),
            add_default=False,
        )

        assert formats._formats == {".test": Path("tests")}

    def test_read_config_with_default(self) -> None:
        formats = read_config(
            config_path=Path("tests/configs/config.json"),
            add_default=True,
        )

        extend_formats = DEFAULT_FORMATS.copy()
        extend_formats[".test"] = Path("tests")

        assert formats._formats == extend_formats

    def test_get_formats_dir(self) -> None:
        assert self.formats.get_formats(Path("tests")) is None

    def test_get_formats_unknown(self) -> None:
        assert self.formats.get_formats(Path("tests.py")) == Path("unknown")

    def test_get_formats_known(self) -> None:
        assert self.formats.get_formats(Path("tests.txt")) == Path("texts")

    def test_check_folder_format_not_found(self) -> None:
        assert self.formats.check_folder_format(Path("tes")) is False

    def test_check_folder_format_found(self) -> None:
        assert self.formats.check_folder_format(Path("texts")) is True
