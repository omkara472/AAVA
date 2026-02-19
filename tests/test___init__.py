import pytest
from src import app

def test___init___basic():
    result = app.__init__(None)
    assert result is not None

def test___init___type():
    result = app.__init__(None)
    assert result is not False
