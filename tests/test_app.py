import pytest
from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_test_login_functionality_returns_value():
    result = app.test_login_functionality(None)
    assert result is not None
