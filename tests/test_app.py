import pytest
from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_login_returns_value():
    result = app.login(None, None, None)
    assert result is not None


def test_verify_dashboard_redirect_returns_value():
    result = app.verify_dashboard_redirect(None)
    assert result is not None


def test_test_login_functionality_returns_value():
    result = app.test_login_functionality(None)
    assert result is not None
