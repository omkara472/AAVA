import pytest
from src import app
 
def test_test_multiply_basic():
    result = app.test_multiply()
    assert result is not None
 
def test_test_multiply_type():
    result = app.test_multiply()
    assert result is not False
