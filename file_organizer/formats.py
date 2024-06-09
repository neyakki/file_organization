"""Описание доступных форматов"""

from __future__ import annotations

from json import load
from logging import Logger, getLogger
from pathlib import Path

from .const import DEFAULT_FORMATS

__all__ = (
    "FormatsFile",
    "read_config",
)


def read_config(
    config_path: Path | None = None,
    logger: Logger | None = None,
    *,
    add_default: bool = False,
) -> FormatsFile:
    """
    Чтение файла конфигурации

    Args:
        config_path: Путь к файлу настроек
        logger: Экземпляр :class: `Logger`
        add_default: Добавить дефолтные настройки

    Returns:
        Экземпляр :class: `FormatsFile`
    """
    logger = logger or getLogger(__name__)
    if not config_path or not config_path.exists():
        return FormatsFile()

    config = load(config_path.open("rb"))

    formats = DEFAULT_FORMATS.copy() if add_default else {}

    if formats_config := config.get("formats"):
        for folder in formats_config.keys():
            folder_path = Path(folder)

            for ext in formats_config[folder]:
                formats[ext] = folder_path
    else:
        logger.warning(
            "Не найден раздел `formats`. Используется конфигурация по умолчанию",
        )

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

    def get_formats(self, name: Path) -> Path | str:
        """
        Получение директории

        Args:
            name: Название файла

        Returns:
            Директория для перемещения
        """
        if name.is_dir():
            return ""

        return self._formats.get(name.suffix.lower(), self._other)

    def check_folder_format(self, name: Path) -> bool:
        """
        Проверка директории

        Args:
            name: Название директории

        Returns:
            Существует ли директория
        """
        return Path(name.stem) in self._folders
