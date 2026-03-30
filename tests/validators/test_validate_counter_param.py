import pytest

from batch_renamer import validators, exceptions


def test_correct_param():
    param = "03d"
    expected = ("0", 3)
    assert validators.validate_counter_param(param) == expected


def test_empty_param():
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_counter_param("")


def test_without_d():
    param = "03"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_counter_param(param)


def test_incorrect_param():
    param = "1d"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_counter_param(param)


def test_incorrect_len():
    param = "-sd"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_counter_param(param)


def test_negative_len():
    param = "0-3d"
    with pytest.raises(exceptions.PatternValidationError):
        validators.validate_counter_param(param)
