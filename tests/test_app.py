from src import app


def test_test_add():
    result = app.test_add()
    assert result is not None

def test_test_multiply():
    result = app.test_multiply()
    assert result is not None

def test_test_divide():
    result = app.test_divide()
    assert result is not None
