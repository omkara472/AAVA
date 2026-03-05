from src import app


def test_driver():
    result = app.driver()
    assert result is not None

def test_test_homepage_title():
    result = app.test_homepage_title(None)
    assert result is not None

def test_test_search_product():
    result = app.test_search_product(None)
    assert result is not None

def test_test_add_to_cart():
    result = app.test_add_to_cart(None)
    assert result is not None

def test_test_cart_button():
    result = app.test_cart_button(None)
    assert result is not None
