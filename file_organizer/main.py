"""Точка запуска утилиты. Управляет и инициализирует компоненты"""

from __future__ import annotations

import argparse
from pathlib import Path

from file_organizer.file_organizer import file_organizer

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


def main() -> None:
    """Точка входа"""
    args = parser.parse_args()

    file_organizer(
        target_dir=args.target_dir.absolute(),
        recursive=args.recursive,
    )
