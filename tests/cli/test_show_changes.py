import pytest
import pathlib

from batch_renamer import cli


def _build_expected(files: pathlib.Path, new_names: str) -> str:
    """
    Формирует строку вывода функции cli.show_changes.
    :param pathlib.Path files: список файлов
    :param str new_names: список новых имен файлов
    :return: str
    """
    max_len = max(len(f.name) for f in files) if files else 0
    return "\n".join(
        f"{f.name:<{max_len}} -> {name}" for f, name in zip(files, new_names)
    ) + ("\n" if files else "")


def test_regular_call(capsys):
    files = [
        pathlib.Path("/tmp/a.txt"),
        pathlib.Path("/tmp/ab.txt"),
        pathlib.Path("/tmp/abc.txt"),
        pathlib.Path("/tmp/abcd.txt"),
    ]
    new_names = ["new_a.txt", "new_b.txt", "new_c.txt", "new_d.txt"]

    max_len = max(len(f.name) for f in files)
    expected = _build_expected(files, new_names)
    cli.show_changes(files, new_names)
    out = capsys.readouterr().out
    assert out == expected


def test_empty_lists(capsys):
    expected = ""
    cli.show_changes([], [])
    out = capsys.readouterr().out
    assert out == expected


def test_long_filename(capsys):
    files = [
        pathlib.Path(
            "/tmp/very_very_very_very_very_very_very_very_very_very_very_very_very_very_very_very_long_name.txt"
        ),
        pathlib.Path("/tmp/name.txt"),
        pathlib.Path("/tmp/name.txt"),
        pathlib.Path("/tmp/name.txt"),
    ]
    new_names = ["new_name1.txt", "new_name2.txt", "new_name3.txt", "new_name4.txt"]

    max_len = max(len(f.name) for f in files)
    expected = _build_expected(files, new_names)
    cli.show_changes(files, new_names)
    out = capsys.readouterr().out
    assert out == expected


def test_special_symbols(capsys):
    files = [
        pathlib.Path("/tmp/файл 1.txt"),
        pathlib.Path("/tmp/файл 2.txt"),
        pathlib.Path("/tmp/файл 3.txt"),
        pathlib.Path("/tmp/файл 4.txt"),
    ]
    new_names = ["new_файл 1.txt", "new_файл 2.txt", "new_файл 3.txt", "new_файл 4.txt"]

    max_len = max(len(f.name) for f in files)
    expected = _build_expected(files, new_names)
    cli.show_changes(files, new_names)
    out = capsys.readouterr().out
    assert out == expected
