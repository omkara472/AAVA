from src import app


def test_add():
    result = app.add(2, 3)
    assert result == 5


def test_multiply():
    result = app.multiply(4, 5)
    assert result == 20