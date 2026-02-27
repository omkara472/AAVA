import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_test_google_title_returns_value():
    result = app.test_google_title(None)
    assert result is not None


def test_test_google_search_box_present_returns_value():
    result = app.test_google_search_box_present(None)
    assert result is not None
