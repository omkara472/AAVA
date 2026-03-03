import pytest
from src import app

def test_test_add_not_none():
    result = app.test_add()
    assert result is not None

def test_test_add_not_false():
    result = app.test_add()
    assert result is not False
