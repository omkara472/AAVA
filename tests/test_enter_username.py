import pytest
from src import app

def test_enter_username_basic():
    result = app.enter_username(None)
    assert result is not None

def test_enter_username_type():
    result = app.enter_username(None)
    assert result is not False
