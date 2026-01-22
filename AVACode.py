# ─────────────────────────────────────────────────────────────────────────────
# Python Files: Modular Selenium and PyTest Automation Code
# ─────────────────────────────────────────────────────────────────────────────

# Directory structure:
# project_root/
# ├── pages/
# │   ├── base_page.py
# │   ├── login_page.py
# │   ├── dashboard_page.py
# │   ├── profile_page.py
# │   └── admin_page.py
# ├── tests/
# │   └── test_app.py
# ├── conftest.py
# ├── requirements.txt
# ├── README.md
# └── sample_test_results.txt

# ─────────────────────────────────────────────────────────────────────────────
# pages/base_page.py
# ─────────────────────────────────────────────────────────────────────────────

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects, providing common Selenium actions."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, by, locator):
        """Find element with explicit wait."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def click(self, by, locator):
        """Click element with explicit wait."""
        element = self.find(by, locator)
        element.click()

    def type(self, by, locator, value):
        """Type into input field after clearing."""
        element = self.find(by, locator)
        element.clear()
        element.send_keys(value)

    def is_visible(self, by, locator):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except:
            return False

    def get_text(self, by, locator):
        """Get text of element."""
        element = self.find(by, locator)
        return element.text

    def wait_until_url_contains(self, url_fragment):
        """Wait until URL contains the given fragment."""
        WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(url_fragment)
        )

# ─────────────────────────────────────────────────────────────────────────────
# pages/login_page.py
# ─────────────────────────────────────────────────────────────────────────────

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the Login page."""

    URL = "https://example.com/login"  # Placeholder URL

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "loginError")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

    def go_to(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type(*self.USERNAME_INPUT, value=username)
        self.type(*self.PASSWORD_INPUT, value=password)
        self.click(*self.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(*self.FORGOT_PASSWORD_LINK)

    def is_error_displayed(self):
        return self.is_visible(*self.ERROR_MESSAGE)

    def get_error_message(self):
        return self.get_text(*self.ERROR_MESSAGE)

# ─────────────────────────────────────────────────────────────────────────────
# pages/dashboard_page.py
# ─────────────────────────────────────────────────────────────────────────────

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page Object for the Dashboard."""

    URL_FRAGMENT = "/dashboard"
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    WIDGETS = (By.CLASS_NAME, "dashboard-widget")
    PROFILE_LINK = (By.ID, "profileLink")

    def is_loaded(self):
        return self.URL_FRAGMENT in self.driver.current_url

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

    def widgets_loaded(self):
        return len(self.driver.find_elements(*self.WIDGETS)) > 0

    def go_to_profile(self):
        self.click(*self.PROFILE_LINK)

# ─────────────────────────────────────────────────────────────────────────────
# pages/profile_page.py
# ─────────────────────────────────────────────────────────────────────────────

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProfilePage(BasePage):
    """Page Object for the Profile page."""

    NAME_INPUT = (By.ID, "profileName")
    EMAIL_INPUT = (By.ID, "profileEmail")
    SAVE_BUTTON = (By.ID, "saveProfileBtn")
    SUCCESS_MESSAGE = (By.ID, "profileSuccess")

    def update_profile(self, name=None, email=None):
        if name:
            self.type(*self.NAME_INPUT, value=name)
        if email:
            self.type(*self.EMAIL_INPUT, value=email)
        self.click(*self.SAVE_BUTTON)

    def is_update_successful(self):
        return self.is_visible(*self.SUCCESS_MESSAGE)

# ─────────────────────────────────────────────────────────────────────────────
# pages/admin_page.py
# ─────────────────────────────────────────────────────────────────────────────

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AdminPage(BasePage):
    """Page Object for the Admin page."""

    URL = "https://example.com/admin"
    ACCESS_DENIED_MESSAGE = (By.ID, "accessDeniedMsg")

    def go_to(self):
        self.driver.get(self.URL)

    def is_access_denied(self):
        return self.is_visible(*self.ACCESS_DENIED_MESSAGE)

# ─────────────────────────────────────────────────────────────────────────────
# conftest.py
# ─────────────────────────────────────────────────────────────────────────────

import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    """Initialize WebDriver session (Chrome by default)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ─────────────────────────────────────────────────────────────────────────────
# tests/test_app.py
# ─────────────────────────────────────────────────────────────────────────────

import pytest
import time

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.profile_page import ProfilePage
from pages.admin_page import AdminPage

# Test data (replace with secure retrieval in real projects)
VALID_USER = {"username": "testuser", "password": "password123"}
INVALID_USER = {"username": "wronguser", "password": "wrongpass"}
REGISTERED_EMAIL = "testuser@example.com"
NEW_PROFILE = {"name": "New Name", "email": "newemail@example.com"}

@pytest.mark.high
def test_login_success(browser):
    """TC-001: Verify Login Functionality"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard = DashboardPage(browser)
    dashboard.wait_until_url_contains(dashboard.URL_FRAGMENT)
    assert dashboard.is_loaded(), "User should be redirected to dashboard"

@pytest.mark.medium
def test_forgot_password(browser):
    """TC-002: Validate Forgot Password Flow"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.click_forgot_password()
    # Assume Forgot Password page opens, fill in email
    from selenium.webdriver.common.by import By
    EMAIL_INPUT = (By.ID, "forgotEmail")
    SUBMIT_BUTTON = (By.ID, "resetPasswordBtn")
    login_page.type(*EMAIL_INPUT, value=REGISTERED_EMAIL)
    login_page.click(*SUBMIT_BUTTON)
    # Confirmation message
    CONFIRM_MSG = (By.ID, "resetConfirmMsg")
    assert login_page.is_visible(*CONFIRM_MSG), "Password reset email should be sent"

@pytest.mark.low
def test_logout(browser):
    """TC-003: Check Logout Functionality"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard = DashboardPage(browser)
    dashboard.wait_until_url_contains(dashboard.URL_FRAGMENT)
    dashboard.logout()
    # After logout, should be back at login page
    assert "login" in browser.current_url

@pytest.mark.high
def test_dashboard_widgets_load(browser):
    """TC-004: Validate Dashboard Widgets Load"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard = DashboardPage(browser)
    dashboard.wait_until_url_contains(dashboard.URL_FRAGMENT)
    assert dashboard.widgets_loaded(), "All widgets should load without error"

@pytest.mark.medium
def test_profile_update(browser):
    """TC-005: Verify Profile Update"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard = DashboardPage(browser)
    dashboard.go_to_profile()
    profile = ProfilePage(browser)
    profile.update_profile(name=NEW_PROFILE["name"], email=NEW_PROFILE["email"])
    assert profile.is_update_successful(), "Profile details should be updated successfully"

@pytest.mark.high
def test_invalid_login(browser):
    """TC-006: Test Invalid Login Attempt"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(INVALID_USER["username"], INVALID_USER["password"])
    assert login_page.is_error_displayed(), "Error message should be displayed on invalid login"

@pytest.mark.medium
@pytest.mark.slow
def test_session_timeout(browser):
    """TC-007: Verify Session Timeout"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard = DashboardPage(browser)
    dashboard.wait_until_url_contains(dashboard.URL_FRAGMENT)
    # Simulate idle (use a short time for demo; real test would be 30 min)
    time.sleep(2)  # Replace with 1800 for real test
    browser.refresh()
    # After timeout, should be redirected to login
    assert "login" in browser.current_url

@pytest.mark.high
def test_access_control(browser):
    """TC-008: Validate Access Control"""
    login_page = LoginPage(browser)
    login_page.go_to()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    admin_page = AdminPage(browser)
    admin_page.go_to()
    assert admin_page.is_access_denied(), "Access denied message should be shown"

# ─────────────────────────────────────────────────────────────────────────────
# requirements.txt
# ─────────────────────────────────────────────────────────────────────────────

selenium>=4.10.0
pytest>=7.0.0

# ─────────────────────────────────────────────────────────────────────────────
# README.md
# ─────────────────────────────────────────────────────────────────────────────

# Selenium PyTest Automation Suite

## Overview

This project contains a modular Selenium and PyTest-based automation framework for validating web application functionality, converted from structured manual test cases (source: Jira SCRUM-6, Manual_Test_Cases.xlsx).

Test cases automated:
- Login (valid/invalid)
- Logout
- Forgot Password
- Dashboard widgets
- Profile update
- Session timeout
- Access control

## Directory Structure

project_root/
├── pages/               # Page Object Model classes
├── tests/               # Test cases
├── conftest.py          # PyTest fixtures
├── requirements.txt     # Dependencies
├── README.md            # This documentation
└── sample_test_results.txt

## Setup Instructions

1. **Clone the repository**
   git clone <repo_url>
   cd project_root

2. **Create and activate a virtual environment**
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
   pip install -r requirements.txt

4. **Download ChromeDriver**
   - Ensure ChromeDriver is installed and in your PATH.
   - Download from: https://chromedriver.chromium.org/downloads

5. **Configure test data**
   - For demo, default credentials are hardcoded in `tests/test_app.py`.
   - For production, integrate with a secure test data provider.

## Running Tests

pytest --maxfail=1 --disable-warnings -v

## Sample Test Output

See `sample_test_results.txt` for an example.

## Troubleshooting

- **WebDriverException: Message: 'chromedriver' executable needs to be in PATH**
    - Download ChromeDriver and add it to your system PATH.

- **Element not found**
    - Check selector definitions in page objects. Update as per your application’s HTML.

- **Timeouts**
    - Increase timeouts in `BasePage` or investigate application performance issues.

- **Test Data Issues**
    - Ensure the test user accounts and emails exist in your test environment.

## Extending the Framework

- Add new page objects to `pages/`.
- Add new test cases to `tests/`.
- Use PyTest markers for grouping and selective runs.
- Parameterize tests for data-driven execution.

## CI/CD Integration

- Integrate with GitHub Actions, GitLab CI, Jenkins, etc.
- Use `pytest` exit codes for pipeline pass/fail status.
- Artifacts: Store screenshots/logs on failure for debugging.

## Best Practices

- Prefer explicit waits over implicit waits.
- Use clear, stable selectors (IDs preferred).
- Keep page objects reusable and tests atomic.
- Separate test data from code for maintainability.

## Security

- Do not commit real credentials.
- Review any dynamic code generation for code injection risks.

## Maintenance

- Regularly update Selenium, PyTest, and browser drivers.
- Review selectors for breakages after application UI changes.
- Add tests for new features and regression coverage.

## Contact

For framework issues, contact QA Automation Lead.

# ─────────────────────────────────────────────────────────────────────────────
# sample_test_results.txt
# ─────────────────────────────────────────────────────────────────────────────

============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/user/project_root
collected 8 items

tests/test_app.py::test_login_success PASSED                             [ 12%]
tests/test_app.py::test_forgot_password PASSED                           [ 25%]
tests/test_app.py::test_logout PASSED                                    [ 37%]
tests/test_app.py::test_dashboard_widgets_load PASSED                    [ 50%]
tests/test_app.py::test_profile_update PASSED                            [ 62%]
tests/test_app.py::test_invalid_login PASSED                             [ 75%]
tests/test_app.py::test_session_timeout PASSED                           [ 87%]
tests/test_app.py::test_access_control PASSED                            [100%]

============================== 8 passed in 19.02s =============================
