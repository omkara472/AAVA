import pytest
from app import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_wait_for_element_returns_value():
    result = app.wait_for_element(None, None, None)
    assert result is not None


def test_test_login_returns_value():
    result = app.test_login(None)
    assert result is not None


def test_test_login_returns_value():
    result = app.test_login(None)
    assert result is not None
