import pytest
from src import app

def test_test_multiply_not_none():
    result = app.test_multiply()
    assert result is not None

def test_test_multiply_not_false():
    result = app.test_multiply()
    assert result is not False
