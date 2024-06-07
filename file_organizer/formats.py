"""Описание доступных форматов"""

from __future__ import annotations

from json import load
from pathlib import Path

from .const import DEFAULT_FORMATS

__all__ = (
    "FormatsFile",
    "read_config",
)


def read_config(config_path: Path | None = None) -> FormatsFile:
    """
    Чтение файла конфигурации

    Args:
        config_path: Путь к файлу настроек

    Returns:
        Экземпляр :class: `FormatsFile`
    """
    if not config_path:
        return FormatsFile()

    config = load(config_path.open("rb"))
    formats = DEFAULT_FORMATS.copy()

    if formats_config := config.get("formats"):
        for folder in formats_config.keys():
            folder_path = Path(folder)

            for ext in formats_config[folder]:
                formats[ext] = folder_path

    return FormatsFile(formats=formats)


class FormatsFile:
    """Класс для работы с директориями форматов файлов"""

    def __init__(
        self,
        formats: dict[str, Path] = DEFAULT_FORMATS,
    ) -> None:
        """
        Конструктор

        Args:
            formats: Доступные форматы. Defaults to DEFAULT_FORMATS.
            folders: Директории форматов. Defaults to DEFAULT_FOLDERS.
        """
        self._formats = formats
        self._folders = set(formats.values())
        self._other = Path("unknown")

    def get_formats(self, name: Path) -> Path | None:
        """
        Получение директории

        Args:
            name: Название файла

        Returns:
            Директория для перемещения
        """
        if name.is_dir():
            return None

        return self._formats.get(name.suffix.lower(), self._other)

    def check_folders_format(self, name: Path) -> bool:
        """
        Проверка директории

        Args:
            name: Название директории

        Returns:
            Существует ли директория
        """
        return Path(name.stem) not in self._folders
