import pytest

from batch_renamer import cli as cli


def test_correct_args(monkeypatch):
    expected_object = cli.Args(path="\\photo", pattern="photo.jpeg", dry_run=True)
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--path", expected_object.path, "--pattern", expected_object.pattern, "--dry-run"]
    )
    assert cli.get_args() == expected_object


def test_default_path(monkeypatch):
    expected_object = cli.Args(path=".", pattern="photo.jpeg", dry_run=True)
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--pattern", expected_object.pattern, "--dry-run"]
    )
    assert cli.get_args() == expected_object


def test_without_dry_run(monkeypatch):
    expected_object = cli.Args(path="\\photo", pattern="photo.jpeg", dry_run=False)
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--path", expected_object.path, "--pattern", expected_object.pattern]
    )
    assert cli.get_args() == expected_object


def test_without_pattern(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py"]
    )
    with pytest.raises(SystemExit):
        cli.get_args()


def test_empty_path(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--path", ""]
    )
    with pytest.raises(SystemExit):
        cli.get_args()


def test_empty_pattern(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--pattern", ""]
    )
    with pytest.raises(SystemExit):
        cli.get_args()


def test_unknown_arg(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--unknown"]
    )
    with pytest.raises(SystemExit):
        cli.get_args()
