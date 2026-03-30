import pytest
import pathlib

from batch_renamer import validators, exceptions


def test_correct_path(tmp_path):
    expected = pathlib.Path(tmp_path)
    assert validators.validate_path(str(tmp_path)) == expected


def test_incorrect_path(tmp_path):
    path = tmp_path / "non_existent_path"
    with pytest.raises(exceptions.PathNotFoundError):
        validators.validate_path(str(path))


def test_path_is_file(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("This is not directory")
    with pytest.raises(exceptions.PathNotDirError):
        validators.validate_path(str(file))
