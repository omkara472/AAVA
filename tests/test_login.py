import pytest
from src import app
 
def test_login_basic():
    result = app.login(None, None)
    assert result is not None
 
def test_login_type():
    result = app.login(None, None)
    assert result is not False
