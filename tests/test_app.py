import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_take_screenshot_returns_value():
    result = app.take_screenshot(None, None)
    assert result is not None


def test_test_registration_returns_value():
    result = app.test_registration(None)
    assert result is not None
