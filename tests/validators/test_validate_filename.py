import pytest

from batch_renamer import validators, exceptions


def test_correct_name():
    filename = "correct_filename.txt"
    assert validators.validate_filename(filename) == None


def test_empty_name():
    filename = ""
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_filename(filename)


@pytest.mark.parametrize(
    "end",
    [
        " ",
        ".",
    ],
)
def test_incorrect_end(end):
    filename = "filename" + end
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_filename(filename)


@pytest.mark.parametrize("chars", ["<", ">", ":", '"', "/", "\\", "|", "?", "*"])
def test_filename_has_forbidden_chars(chars):
    filename = "file" + chars + "name"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_filename(filename)


@pytest.mark.parametrize("names", validators._get_forbidden_names())
def test_filename_is_forbidden_names(names):
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_filename(names)

    name_with_expansion = names + ".txt"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_filename(name_with_expansion)


def test_start_point():
    filename = ".filename"
    assert validators.validate_filename(filename) == None
