from src import app


def test_driver():
    result = app.driver()
    assert result is not None

def test_test_verify_login_functionality():
    result = app.test_verify_login_functionality(None)
    assert result is not None
