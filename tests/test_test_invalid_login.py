import pytest
from src import app
 
def test_test_invalid_login_basic():
    result = app.test_invalid_login()
    assert result is not None
 
def test_test_invalid_login_type():
    result = app.test_invalid_login()
    assert result is not False
