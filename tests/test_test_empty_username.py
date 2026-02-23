import pytest
from src import app
 
def test_test_empty_username_basic():
    result = app.test_empty_username()
    assert result is not None
 
def test_test_empty_username_type():
    result = app.test_empty_username()
    assert result is not False
