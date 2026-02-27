import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import app

def test_test_google_title_returns_value():
    result = app.test_google_title()
    assert result is not None
