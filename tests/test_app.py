import pytest
from src import app

def test_test_add_returns_value():
    result = app.test_add()
    assert result is not None


def test_test_subtract_returns_value():
    result = app.test_subtract()
    assert result is not None
