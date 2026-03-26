import pytest

from batch_renamer import cli


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("Y", True),
        ("y", True),
        ("N", False),
        ("n", False),
        ("", False),
        ("abc", False),
    ]
)
def test_get_changes_accept(monkeypatch, user_input, expected):
    monkeypatch.setattr("builtins.input", lambda prompt: user_input)
    assert cli.get_changes_accept() == expected
