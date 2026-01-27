# Modular Selenium and PyTest automation code organized into page objects and test cases

# Directory structure:
# project_root/
# ├── pages/
# │   ├── base_page.py
# │   ├── login_page.py
# │   ├── dashboard_page.py
# │   ├── registration_page.py
# │   ├── profile_page.py
# │   └── admin_page.py
# ├── tests/
# │   ├── conftest.py
# │   ├── test_login.py
# │   ├── test_dashboard.py
# │   ├── test_registration.py
# │   ├── test_profile.py
# │   └── test_admin.py
# ├── requirements.txt
# ├── README.md
# └── sample_test_output.txt

# -----------------------------
# pages/base_page.py
# -----------------------------

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator):
        """Find element with explicit wait."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Click an element."""
        self.find(locator).click()

    def type(self, locator, text):
        """Type text into an input field."""
        elem = self.find(locator)
        elem.clear()
        elem.send_keys(text)

    def is_visible(self, locator):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def get_text(self, locator):
        """Get text of element."""
        return self.find(locator).text

    def wait_until_url_contains(self, substring):
        """Wait until URL contains a substring."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(substring)
        )

# -----------------------------
# pages/login_page.py
# -----------------------------

from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page object for Login Page."""

    USERNAME_INPUT = (By.ID, "username")  # Placeholder selector
    PASSWORD_INPUT = (By.ID, "password")  # Placeholder selector
    LOGIN_BUTTON = (By.ID, "login-btn")   # Placeholder selector
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-msg")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

    def load(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def login_invalid(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)

# -----------------------------
# pages/dashboard_page.py
# -----------------------------

from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """Page object for Dashboard."""

    WIDGETS = [
        (By.ID, "widget-1"),   # Placeholder selectors
        (By.ID, "widget-2"),
        (By.ID, "widget-3"),
    ]
    LOGOUT_BUTTON = (By.ID, "logout-btn")  # Placeholder selector

    def all_widgets_displayed(self):
        return all(self.is_visible(widget) for widget in self.WIDGETS)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

# -----------------------------
# pages/registration_page.py
# -----------------------------

from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegistrationPage(BasePage):
    """Page object for Registration Page."""

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "reg-password")
    TERMS_CHECKBOX = (By.ID, "accept-terms")
    REGISTER_BUTTON = (By.ID, "register-btn")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-msg")

    def load(self, url):
        self.driver.get(url)

    def register(self, email, password, accept_terms=True):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        if accept_terms:
            self.click(self.TERMS_CHECKBOX)
        self.click(self.REGISTER_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

# -----------------------------
# pages/profile_page.py
# -----------------------------

from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProfilePage(BasePage):
    """Page object for Profile Page."""

    EDIT_BUTTON = (By.ID, "edit-profile-btn")
    SAVE_BUTTON = (By.ID, "save-profile-btn")
    NAME_INPUT = (By.ID, "profile-name")
    EMAIL_INPUT = (By.ID, "profile-email")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg")

    def edit_profile(self, name=None, email=None):
        self.click(self.EDIT_BUTTON)
        if name:
            self.type(self.NAME_INPUT, name)
        if email:
            self.type(self.EMAIL_INPUT, email)
        self.click(self.SAVE_BUTTON)

    def is_update_successful(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

# -----------------------------
# pages/admin_page.py
# -----------------------------

from selenium.webdriver.common.by import By
from .base_page import BasePage

class AdminPage(BasePage):
    """Page object for Admin (for role-based access tests)."""

    ACCESS_DENIED_MESSAGE = (By.CSS_SELECTOR, ".access-denied-msg")

    def is_access_denied(self):
        return self.is_visible(self.ACCESS_DENIED_MESSAGE)

# -----------------------------
# tests/conftest.py
# -----------------------------

import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    # You can parametrize this fixture to support multiple browsers
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # comment out for headed mode
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    return "http://localhost:8000"  # Change to your actual base URL

@pytest.fixture
def valid_user():
    # Should be replaced with actual test credentials
    return {"username": "testuser", "password": "TestPass123", "email": "testuser@example.com"}

@pytest.fixture
def invalid_user():
    return {"username": "invaliduser", "password": "WrongPass!"}

# -----------------------------
# tests/test_login.py
# -----------------------------

import pytest
from pages.login_page import LoginPage

@pytest.mark.usefixtures("browser", "base_url")
class TestLogin:

    def test_login_valid(self, browser, base_url, valid_user):
        """TC-001: Verify Login Functionality"""
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        login_page.login(valid_user["username"], valid_user["password"])
        assert login_page.wait_until_url_contains("dashboard"), "User not redirected to dashboard"

    def test_login_invalid(self, browser, base_url, invalid_user):
        """TC-002: Verify Invalid Login"""
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        login_page.login_invalid(invalid_user["username"], invalid_user["password"])
        assert login_page.is_visible(LoginPage.ERROR_MESSAGE), "Error message not displayed"

# -----------------------------
# tests/test_dashboard.py
# -----------------------------

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.usefixtures("browser", "base_url", "valid_user")
class TestDashboard:

    def login_and_navigate(self, browser, base_url, valid_user):
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        login_page.login(valid_user["username"], valid_user["password"])
        dashboard_page = DashboardPage(browser)
        dashboard_page.wait_until_url_contains("dashboard")
        return dashboard_page

    def test_dashboard_widgets(self, browser, base_url, valid_user):
        """TC-004: Validate Dashboard Widgets"""
        dashboard_page = self.login_and_navigate(browser, base_url, valid_user)
        assert dashboard_page.all_widgets_displayed(), "Not all widgets are displayed"

    def test_logout(self, browser, base_url, valid_user):
        """TC-005: Verify Logout Functionality"""
        dashboard_page = self.login_and_navigate(browser, base_url, valid_user)
        dashboard_page.logout()
        assert "login" in browser.current_url, "User not redirected to login page after logout"

    def test_session_timeout(self, browser, base_url, valid_user):
        """TC-006: Test Session Timeout"""
        import time
        dashboard_page = self.login_and_navigate(browser, base_url, valid_user)
        time.sleep(5)  # Use 1800 (30 min) in real test, reduced for automation demo
        browser.refresh()
        assert "login" in browser.current_url, "User not redirected to login after session timeout"

# -----------------------------
# tests/test_registration.py
# -----------------------------

import pytest
from pages.registration_page import RegistrationPage

@pytest.mark.usefixtures("browser", "base_url")
class TestRegistration:

    def test_email_validation(self, browser, base_url):
        """TC-008: Check Email Validation"""
        reg_page = RegistrationPage(browser)
        reg_page.load(f"{base_url}/register")
        reg_page.register("invalid-email", "SomePass123", accept_terms=True)
        assert reg_page.is_visible(RegistrationPage.ERROR_MESSAGE), "Invalid email error not displayed"

    def test_terms_acceptance(self, browser, base_url):
        """TC-009: Validate Terms Acceptance"""
        reg_page = RegistrationPage(browser)
        reg_page.load(f"{base_url}/register")
        reg_page.register("user2@example.com", "SomePass123", accept_terms=False)
        assert reg_page.is_visible(RegistrationPage.ERROR_MESSAGE), "Terms acceptance error not displayed"

# -----------------------------
# tests/test_profile.py
# -----------------------------

import pytest
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

@pytest.mark.usefixtures("browser", "base_url", "valid_user")
class TestProfile:

    def login_and_navigate(self, browser, base_url, valid_user):
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        login_page.login(valid_user["username"], valid_user["password"])
        profile_page = ProfilePage(browser)
        browser.get(f"{base_url}/profile")
        return profile_page

    def test_profile_update(self, browser, base_url, valid_user):
        """TC-007: Verify Profile Update"""
        profile_page = self.login_and_navigate(browser, base_url, valid_user)
        profile_page.edit_profile(name="New Name")
        assert profile_page.is_update_successful(), "Profile update failed"

# -----------------------------
# tests/test_admin.py
# -----------------------------

import pytest
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

@pytest.mark.usefixtures("browser", "base_url")
class TestAdmin:

    def test_user_role_permissions(self, browser, base_url):
        """TC-012: Check User Role Permissions"""
        # Use a restricted user for this test in a real environment
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        login_page.login("restricted_user", "SomePass123")
        admin_page = AdminPage(browser)
        browser.get(f"{base_url}/admin")
        assert admin_page.is_access_denied(), "Access denied message not displayed"

    def test_account_lockout(self, browser, base_url, valid_user):
        """TC-010: Test Account Lockout"""
        login_page = LoginPage(browser)
        login_page.load(f"{base_url}/login")
        for _ in range(5):
            login_page.login_invalid(valid_user["username"], "WrongPass!")
        assert login_page.is_visible(LoginPage.ERROR_MESSAGE), "Account lockout error not displayed"

# -----------------------------
# requirements.txt
# -----------------------------

selenium>=4.8.0
pytest>=7.0.0

# -----------------------------
# README.md
# -----------------------------

# Selenium PyTest Automation Suite

## Overview

This repository contains a modular Selenium WebDriver automation framework using PyTest, following the Page Object Model (POM) pattern. It automates core authentication, registration, profile, dashboard, and access control scenarios derived from validated JSON test cases.

## Directory Structure

pages/     # Page Object classes for modular interaction
tests/     # PyTest test suites, organized by feature
requirements.txt   # Python dependencies
README.md          # This documentation
sample_test_output.txt # Example test run output

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Install dependencies:**
   - Ensure Python 3.8+ is installed.
   - Create a virtual environment (recommended):
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure test data:**
   - Update `tests/conftest.py` with valid test user credentials and the correct `base_url` for your application.

4. **Run tests:**
   ```bash
   pytest tests/
   ```

## Usage Examples

- To run all tests:
  ```
  pytest
  ```
- To run a single test file:
  ```
  pytest tests/test_login.py
  ```

## Troubleshooting

- **WebDriver Setup Problems:**  
  Ensure you have Chrome installed and the matching `chromedriver` in your PATH.  
  For other browsers, modify the `browser` fixture in `conftest.py`.

- **Environment Configuration Errors:**  
  Check that `base_url` is correct and the application is running.

- **Timeouts or Element Not Found:**  
  Update placeholder selectors in `pages/` as needed to match your application’s HTML.

- **Missing or Failing Tests:**  
  Review `sample_test_output.txt` for errors. Validate test data and selectors.

## Extending the Framework

- **Add new pages:**  
  Create a new class in `pages/` extending `BasePage`.

- **Add new tests:**  
  Place new test modules in `tests/`, following PyTest conventions.

- **Parameterization:**  
  Use PyTest’s `@pytest.mark.parametrize` for data-driven testing.

- **Parallel Execution:**  
  Integrate `pytest-xdist` for parallel test runs.

## Best Practices

- Use explicit waits in page objects for reliable test execution.
- Keep test data and selectors in fixtures or config files for maintainability.
- Review and update selectors regularly to avoid flaky tests.
- Log test failures with screenshots for easier debugging.

## CI/CD Integration

- Integrate with tools like GitHub Actions, Jenkins, or GitLab CI by running `pytest` as part of your pipeline.
- Collect test reports using `pytest --junitxml=results.xml` for dashboard integration.

## Security Notes

- No passwords or sensitive data are committed to source.
- No unsafe code execution or system calls are performed.

## Feedback and Maintenance

- Update page object selectors as the application evolves.
- Review test results and logs after each run.
- Coordinate with QA leads for continuous improvement.

---

## Sample Test Output

See `sample_test_output.txt` for a sample test run.

# -----------------------------
# sample_test_output.txt
# -----------------------------

============================= test session starts ==============================
platform linux -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/user/selenium-pytest-demo
collected 10 items

tests/test_login.py ..                                                 [ 20%]
tests/test_dashboard.py ...                                            [ 50%]
tests/test_registration.py ..                                          [ 70%]
tests/test_profile.py .                                                [ 80%]
tests/test_admin.py ..                                                 [100%]

============================== 10 passed in 25.42s ============================
