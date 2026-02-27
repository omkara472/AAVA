import pytest
from src import app

def test_test_add_returns_value():
    result = app.test_add()
    assert result is not None


def test_test_multiply_returns_value():
    result = app.test_multiply()
    assert result is not None
