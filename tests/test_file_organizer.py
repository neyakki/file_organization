"""Тестирование сортировки файлов"""

from __future__ import annotations

from logging import Logger
from pathlib import Path
from uuid import uuid4

import pytest
from pytest_mock.plugin import MockerFixture

from file_organizer.file_organizer import FileOrganizer
from file_organizer.formats import FormatsFile


@pytest.fixture()
def organizer(mocker: MockerFixture) -> FileOrganizer:
    formats = FormatsFile()
    logger = mocker.MagicMock(Logger)

    return FileOrganizer(
        format_file=formats,
        logger=logger,
    )


class TestOrganizer:
    """Тестирование сортировки файлов"""

    @pytest.mark.parametrize(
        "file,spec",
        (
            [Path("test.txt"), Path("texts")],
            [Path("test.bs"), Path("unknown")],
        ),
    )
    def test_organizer(
        self,
        file: Path,
        spec: Path | str,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        target_dir = Path("test")

        mock_list_dir = mocker.patch.object(organizer, "_list_dir")
        mock_create_dir = mocker.patch.object(organizer, "_create_dir")
        mock_move_file = mocker.patch.object(organizer, "_move_file")
        mocker.patch.object(organizer, "_remove_empty_folder")

        mock_list_dir.return_value = [target_dir / file]

        organizer.organizer(
            target_dir=target_dir,
            recursive=False,
        )

        mock_list_dir.assert_called_once_with(
            target_dir,
            recursive=False,
        )
        mock_create_dir.assert_called_once_with(target_dir / spec)
        mock_move_file.assert_called_once_with(
            src=target_dir / file,
            dst=target_dir / spec,
        )

    def test_list_dir(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_path = mocker.patch("file_organizer.file_organizer.Path")
        expected = [mock_path("test.txt") for _ in range(10)]
        mock_path.return_value.iterdir.return_value = expected
        mock_path.return_value.is_dir.return_value = False

        retval = organizer._list_dir(name=mock_path("test"))

        assert list(retval) == list(map(mock_path, expected))

    def test_create_dir(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_path = mocker.patch("file_organizer.file_organizer.Path")

        mock_path.return_value.exists.return_value = False

        organizer._create_dir(name=mock_path("test"))
        mock_path.return_value.mkdir.assert_called_once_with(parents=True)

    def test_create_dir_exists(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_path = mocker.patch("file_organizer.file_organizer.Path")

        mock_path.return_value.exists.return_value = True

        organizer._create_dir(name=mock_path("test"))
        mock_path.return_value.mkdir.assert_not_called()

    def test_remove_empty_folder(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_path = mocker.patch("file_organizer.file_organizer.Path")

        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.rmdir.return_value = True
        mock_path.return_value.iterdir.return_value = []

        organizer._remove_empty_folder(name=mock_path("test"))
        mock_path.return_value.rmdir.assert_called_once()

    def test_remove_empty_folder_not_empty(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_path = mocker.patch("file_organizer.file_organizer.Path")

        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.rmdir.return_value = True
        mock_path.return_value.iterdir.return_value = [str(uuid4())]

        organizer._remove_empty_folder(name=mock_path("test"))
        mock_path.return_value.rmdir.assert_not_called()

    def test_move_file_exists(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_move = mocker.patch("shutil.move")
        mock_path = mocker.patch("file_organizer.file_organizer.Path")
        file = mock_path(f"{uuid4}.txt")

        mock_path.return_value.__truediv__.return_value.exists.return_value = True
        mock_path.return_value.rename.return_value = file

        organizer._move_file(
            src=mock_path("test.txt"),
            dst=mock_path("test"),
        )
        mock_move.assert_called_once_with(
            src=file.as_posix(),
            dst=mock_path("test").as_posix(),
        )

    def test_move_file(
        self,
        organizer: FileOrganizer,
        mocker: MockerFixture,
    ) -> None:
        mock_move = mocker.patch("shutil.move")
        mock_path = mocker.patch("file_organizer.file_organizer.Path")

        mock_path.return_value.__truediv__.return_value.exists.return_value = False

        organizer._move_file(
            src=mock_path("test1.txt"),
            dst=mock_path("test"),
        )
        mock_move.assert_called_once_with(
            src=mock_path("test1.txt").as_posix(),
            dst=mock_path("test").as_posix(),
        )
