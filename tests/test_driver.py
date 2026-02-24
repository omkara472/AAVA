import pytest
from src import app

def test_driver_basic():
    result = app.driver()
    assert result is not None

def test_driver_not_false():
    result = app.driver()
    assert result is not False
