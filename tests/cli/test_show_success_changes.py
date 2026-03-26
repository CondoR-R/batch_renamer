import pytest

from batch_renamer import cli

@pytest.mark.parametrize(
    "count",
    [
        0,
        1000,
        1_000_000,
    ],
)
def test_regular_call(capsys, count):
    cli.show_success_changes(count)
    out = capsys.readouterr().out
    assert out == f"Успешно переименовано {count} файл(-а)(-ов)\n"
