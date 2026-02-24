import pytest
from src import app

def test_test_valid_login_returns_value():
    result = app.test_valid_login(None)
    assert result is not None
