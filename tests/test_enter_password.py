import pytest
from src import app

def test_enter_password_basic():
    result = app.enter_password(None)
    assert result is not None

def test_enter_password_type():
    result = app.enter_password(None)
    assert result is not False
