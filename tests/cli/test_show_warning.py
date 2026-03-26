import pytest

from batch_renamer import cli


@pytest.mark.parametrize(
    "message",
    [
        "Предупреждение 1",
        "Предупреждение 2",
        str(OSError()),
    ],
)
def test_show_warning(capsys, message):
    cli.show_warning(message)
    out, err = capsys.readouterr()
    assert out == f"ПРЕДУПРЕЖДЕНИЕ: {message}\n"
    assert err == ""
