import pytest
from src import app

def test_add():
    result = app.add(None, None)
    assert result is not None

def test_test_add_positive_numbers():
    result = app.test_add_positive_numbers()
    assert result is not None

