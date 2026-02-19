import pytest
from src import app

def test_get_error_message_basic():
    result = app.get_error_message()
    assert result is not None

def test_get_error_message_type():
    result = app.get_error_message()
    assert result is not False
