"""Описание доступных форматов"""

from __future__ import annotations

from pathlib import Path

__all__ = (
    "DEFAULT_FORMATS",
)

tables = Path("tables")
texts = Path("texts")
presentations = Path("presentations")
pdf = Path("pdf")
e_books = Path("e_books")
images = Path("images")
archives = Path("archives")
media = Path("media")
configs = Path("configs")
markup = Path("markup")


DEFAULT_FORMATS = {
    # tables
    ".xlsx": tables,
    ".xls": tables,
    ".csv": tables,
    ".ods": tables,
    # txt
    ".doc": texts,
    ".docx": texts,
    ".odt": texts,
    ".rtf": texts,
    ".txt": texts,
    # presentations
    ".ppt": presentations,
    ".pptx": presentations,
    ".odp": presentations,
    # pdf
    ".pdf": pdf,
    # e-books
    ".epub": e_books,
    ".mobi": e_books,
    ".azw": e_books,
    # image
    ".jpeg": images,
    ".jpg": images,
    ".png": images,
    ".gif": images,
    ".svg": images,
    # archive
    ".tar.gz": archives,
    ".zip": archives,
    ".rar": archives,
    ".7z": archives,
    # media
    ".mp3": media,
    ".mp4": media,
    ".avi": media,
    ".mov": media,
    # config
    ".json": configs,
    ".yaml": configs,
    ".yml": configs,
    ".ini": configs,
    # markup
    ".xml": markup,
    ".html": markup,
    ".md": markup,
}
