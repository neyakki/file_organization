"""Точка запуска утилиты. Управляет и инициализирует компоненты"""

from __future__ import annotations

import argparse
from pathlib import Path

from file_organizer.file_organizer import FileOrganizer
from file_organizer.formats import read_config
from file_organizer.logger import get_logger

parser = argparse.ArgumentParser(
    prog="FileOrganizer",
    description=(
        "Утилита позволяет организовывать файлы в определенной папке, согласно заданным правилам"
    ),
)

parser.add_argument(
    "--target-dir",
    default=Path("."),
    type=Path,
    help="Директория, в которой происходит сортировка. По умолчанию текущая директория",
)
parser.add_argument(
    "--recursive",
    default=False,
    const=True,
    nargs="?",
    help="Рекурсивный обход директории",
)
parser.add_argument(
    "--config-file",
    default=None,
    type=Path,
    help="Директория, в которой происходит сортировка. По умолчанию текущая директория",
)


def main() -> None:
    """Точка входа"""
    args = parser.parse_args()
    organizer = FileOrganizer(
        format_file=read_config(args.config_file),
        logger=get_logger(),
    )

    organizer.organizer(
        target_dir=args.target_dir,
        recursive=args.recursive,
    )


if __name__ == "__main__":
    main()
