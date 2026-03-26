import pytest
import pathlib

import batch_renamer.exceptions as exceptions
from batch_renamer import cli


@pytest.mark.parametrize(
    "exception",
    [
        exceptions.PathNotFoundError(pathlib.Path("tmp/test")),
        exceptions.PatternValidationError("msg"),
        OSError(),
    ],
)
def test_show_error(capsys, exception):
    cli.show_error(exception)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == f"ОШИБКА: {exception}\n"
