import pytest
from src import app

def test_test_scrum_6_login_basic():
    result = app.test_scrum_6_login(None)
    assert result is not None

def test_test_scrum_6_login_type():
    result = app.test_scrum_6_login(None)
    assert result is not False
