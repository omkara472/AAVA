import pytest
from src import app

def test_click_login_basic():
    result = app.click_login()
    assert result is not None

def test_click_login_type():
    result = app.click_login()
    assert result is not False
