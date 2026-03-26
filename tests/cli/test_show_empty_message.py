import pytest
import pathlib

from batch_renamer import cli


def test_regular_call(capsys):
    dir = pathlib.Path("tmp/test")
    cli.show_empty_message(dir)
    out = capsys.readouterr().out
    assert out == f"В директории {dir} отсутствуют файлы\n"

def test_path_with_symbols(capsys):
    dir = pathlib.Path("tmp dir/test'/мои тесты")
    cli.show_empty_message(dir)
    out = capsys.readouterr().out
    assert out == f"В директории {dir} отсутствуют файлы\n"
