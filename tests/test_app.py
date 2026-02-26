import pytest
from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_test_user_registration_flow_returns_value():
    result = app.test_user_registration_flow(None)
    assert result is not None
