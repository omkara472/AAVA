import pytest
from src import app

def test_test_divide_not_none():
    result = app.test_divide()
    assert result is not None

def test_test_divide_not_false():
    result = app.test_divide()
    assert result is not False
