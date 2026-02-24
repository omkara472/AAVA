import pytest
from src import app

def test_test_invalid_login_returns_value():
    result = app.test_invalid_login(None, None, None)
    assert result is not None
