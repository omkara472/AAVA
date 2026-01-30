"""
BasePage: Contains common Selenium actions and utilities for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find_element(self, locator):
        """Wait for presence of element located by locator and return it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Wait for element to be clickable and click."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        """Wait for element, clear and enter text."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except Exception:
            return False

    def get_current_url(self):
        return self.driver.current_url


"""
LoginPage: Page object for login functionality.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "http://example.com/login"  # Placeholder URL

    # Placeholder locators (update as per actual app)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")

    def go_to(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)


"""
DashboardPage: Page object for dashboard after login.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    # Placeholder locator for a dashboard element
    DASHBOARD_INDICATOR = (By.ID, "dashboardWelcome")

    def is_loaded(self):
        """Check if dashboard is loaded by verifying indicator element."""
        return self.is_element_present(self.DASHBOARD_INDICATOR)


"""
ForgotPasswordPage: Page object for password reset.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class ForgotPasswordPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_BUTTON = (By.ID, "submitBtn")
    SUCCESS_MESSAGE = (By.ID, "resetSuccess")  # Placeholder

    def reset_password(self, email):
        self.enter_text(self.EMAIL_INPUT, email)
        self.click(self.SUBMIT_BUTTON)

    def is_reset_successful(self):
        return self.is_element_present(self.SUCCESS_MESSAGE)


"""
LogoutPage: Page object for logout functionality.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class LogoutPage(BasePage):
    LOGOUT_BUTTON = (By.ID, "logoutBtn")

    def logout(self):
        self.click(self.LOGOUT_BUTTON)


"""
Test case for verifying login functionality.
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.smoke
def test_login_valid_user(driver, test_data):
    """
    Steps:
    1. Navigate to login page
    2. Enter valid credentials
    3. Click login button
    Expected Result: User is redirected to dashboard
    """
    login_page = LoginPage(driver)
    login_page.go_to()
    login_page.login(test_data["valid_username"], test_data["valid_password"])

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard did not load after login"


"""
Test case for validating password reset.
"""

import pytest
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage

@pytest.mark.regression
def test_password_reset(driver, test_data):
    """
    Steps:
    1. Click on 'Forgot Password' link
    2. Enter registered email address
    3. Submit request
    4. Check email for reset link
    5. Reset password using link
    Expected Result: Password is reset and user can login with new password
    """
    login_page = LoginPage(driver)
    login_page.go_to()
    login_page.click_forgot_password()

    forgot_page = ForgotPasswordPage(driver)
    forgot_page.reset_password(test_data["valid_email"])

    assert forgot_page.is_reset_successful(), "Password reset was not successful"

    # Simulate checking email and resetting password (mock or manual step)
    # For demo, assume password reset is successful and login with new password
    login_page.go_to()
    login_page.login(test_data["valid_username"], test_data["new_password"])

    # Validate login with new password
    from pages.dashboard_page import DashboardPage
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard did not load after password reset login"


"""
Test case for testing logout functionality.
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.logout_page import LogoutPage

@pytest.mark.sanity
def test_logout(driver, test_data):
    """
    Steps:
    1. Login to application
    2. Click logout button
    Expected Result: User is logged out and redirected to login page
    """
    login_page = LoginPage(driver)
    login_page.go_to()
    login_page.login(test_data["valid_username"], test_data["valid_password"])

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard did not load before logout"

    logout_page = LogoutPage(driver)
    logout_page.logout()

    # After logout, should be redirected to login page
    assert "login" in driver.current_url.lower(), "User was not redirected to login page after logout"


"""
PyTest fixtures for Selenium WebDriver setup and test data.
"""

import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def driver():
    # Change browser as needed: Chrome, Firefox, etc.
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Comment out if you want to see browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def test_data():
    """
    Provides test data for login and password reset.
    Replace with secure test credentials/environment variables in production.
    """
    return {
        "valid_username": "testuser",
        "valid_password": "Test@1234",
        "valid_email": "testuser@example.com",
        "new_password": "NewPass@1234"
    }

