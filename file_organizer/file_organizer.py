"""Модуль организации файлов"""

from __future__ import annotations

import shutil
from collections.abc import Generator
from pathlib import Path

from .formats import folders, formats

__all__ = ("file_organizer",)


def file_organizer(target_dir: Path, recursive: bool = False) -> None:
    """Организация файлов"""
    for name in list_dir(target_dir, recursive=recursive):
        if _dir := formats.get(name.suffix.lower()):
            _dir = target_dir / _dir
            create_dir(_dir)
            move_file(src=name, dst=_dir)

        if name.parent != target_dir:
            remove_empty_folder(name=name.parent)


def list_dir(
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
        if path.is_dir() and Path(path.stem) not in folders:
            if recursive:
                yield from list_dir(
                    name=path,
                    recursive=True,
                )
            else:
                continue

        yield path


def create_dir(name: Path) -> None:
    """
    Создание директории если ее нет

    Args:
        name: Директория
    """
    if not name.exists():
        name.mkdir()
        print(f"Создана директория {name}")


def remove_empty_folder(name: Path) -> None:
    """
    Удаление пустых директорий

    Args:
        name: Название директории
    """
    if name.exists() and name.is_dir() and not tuple(name.iterdir()):
        name.rmdir()
        print(f"Директория {name} удалена")


def move_file(src: Path, dst: Path) -> None:
    """
    Перемещение файлов

    Args:
        src: Что перенести
        dst: Куда перенести
    """
    print(f"Файл перемещен {src.as_posix()} -> {dst.as_posix()}")
    shutil.move(
        src=src.as_posix(),
        dst=dst.as_posix(),
    )
