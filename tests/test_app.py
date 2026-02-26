import pytest
from src import app

def test_add_returns_value():
    result = app.add(None, None)
    assert result is not None


def test_subtract_returns_value():
    result = app.subtract(None, None)
    assert result is not None


def test_test_add_positive_numbers_returns_value():
    result = app.test_add_positive_numbers()
    assert result is not None


def test_test_add_negative_numbers_returns_value():
    result = app.test_add_negative_numbers()
    assert result is not None


def test_test_subtract_positive_numbers_returns_value():
    result = app.test_subtract_positive_numbers()
    assert result is not None


def test_test_subtract_result_negative_returns_value():
    result = app.test_subtract_result_negative()
    assert result is not None
