import pytest
from src import app

def test_driver():
    result = app.driver()
    assert result is not None

def test_test_scrum_6_login():
    result = app.test_scrum_6_login(None)
    assert result is not None

