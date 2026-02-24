import pytest
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(driver):
    login = LoginPage(driver)
    login.load()
    login.enter_username("validUser")
    login.enter_password("validPass")
    login.click_login()

    assert "dashboard" in driver.current_url


@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password",
    [
        ("invalidUser", "invalidPass"),
        ("", "password123"),
        ("user123", "")
    ]
)
def test_invalid_login(driver, username, password):
    login = LoginPage(driver)
    login.load()
    login.enter_username(username)
    login.enter_password(password)
    login.click_login()

    assert "Invalid credentials" in login.get_error_message()