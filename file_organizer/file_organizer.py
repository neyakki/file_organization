"""Модуль организации файлов"""

from __future__ import annotations

import shutil
from collections.abc import Generator
from logging import Logger, getLogger
from pathlib import Path
from uuid import uuid4

from .formats import FormatsFile

__all__ = ("FileOrganizer",)


class FileOrganizer:
    """Организация файлов в каталоге"""

    def __init__(
        self,
        format_file: FormatsFile,
        logger: Logger | None = None,
    ):
        """
        Конструктор

        Args:
            format_file: Экземпляр :class: `FormatFile`
            logger: Экземпляр :class: `Logger`. Defaults to None.
        """
        self._format_file = format_file
        self._logger = logger or getLogger(__name__)

    def organizer(
        self,
        target_dir: Path,
        recursive: bool = False,
    ) -> None:
        """
        Организация файлов

        Args:
            target_dir: Целевая директория
            recursive: Рекурсивный обход файлов. Defaults to False.
        """
        for name in self._list_dir(target_dir, recursive=recursive):
            if _dir := self._format_file.get_formats(name):
                _dir = target_dir / _dir
                self._create_dir(_dir)
                self._move_file(src=name, dst=_dir)

            if name.parent != target_dir:
                self._remove_empty_folder(name=name.parent)

    def _list_dir(
        self,
        name: Path,
        *,
        recursive: bool = False,
    ) -> Generator[Path, None, None]:
        """
        Получение файлов из целевой директории

        Args:
            name: Название целевой директории
            recursive: Рекурсивное получение файлов
        """
        for path in name.iterdir():
            if path.is_dir() and self._format_file.check_folders_format(path):
                if recursive:
                    yield from self._list_dir(
                        name=path,
                        recursive=True,
                    )
                else:
                    continue

            yield path

    def _create_dir(self, name: Path) -> None:
        """
        Создание директории если ее нет

        Args:
            name: Директория
        """
        if not name.exists():
            name.mkdir(parents=True)
            self._logger.info(f"Создана директория {name}")

    def _remove_empty_folder(self, name: Path) -> None:
        """
        Удаление пустых директорий

        Args:
            name: Название директории
        """
        if name.exists() and name.is_dir() and not tuple(name.iterdir()):
            name.rmdir()
            self._logger.info(f"Директория {name} удалена")

    def _move_file(self, src: Path, dst: Path) -> None:
        """
        Перемещение файлов

        Args:
            src: Что перенести
            dst: Куда перенести
        """
        if (dst / src.name).exists():
            src = src.rename(Path(f"{uuid4()}_{src.name}"))
            self._logger.warning(
                f"Файл существует название изменено {src.as_posix()} -> {dst.as_posix()}"
            )

        shutil.move(
            src=src.as_posix(),
            dst=dst.as_posix(),
        )
        self._logger.info(f"Файл перемещен {src.as_posix()} -> {dst.as_posix()}")
