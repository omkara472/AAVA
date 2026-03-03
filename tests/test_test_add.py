import pytest
from src import app
 
def test_test_add_basic():
    result = app.test_add()
    assert result is not None
 
def test_test_add_type():
    result = app.test_add()
    assert result is not False
