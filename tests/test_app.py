from src import app


def test_driver():
    result = app.driver()
    assert result is not None

def test_test_user_registration():
    result = app.test_user_registration(None)
    assert result is not None
