import pytest
from src import app

def test_test_add_positive_returns_value():
    result = app.test_add_positive()
    assert result is not None


def test_test_add_negative_returns_value():
    result = app.test_add_negative()
    assert result is not None


def test_test_subtract_returns_value():
    result = app.test_subtract()
    assert result is not None


def test_test_is_even_true_returns_value():
    result = app.test_is_even_true()
    assert result is not None


def test_test_is_even_false_returns_value():
    result = app.test_is_even_false()
    assert result is not None
