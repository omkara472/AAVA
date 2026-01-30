# Test Automation Suite

This repository contains a modular, maintainable Selenium WebDriver and PyTest automation suite generated from structured manual test cases. The framework is designed using the Page Object Model (POM) and supports easy extension and robust reporting.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)
- [Sample Test Results](#sample-test-results)
- [Troubleshooting](#troubleshooting)
- [Extending the Framework](#extending-the-framework)
- [Best Practices & Recommendations](#best-practices--recommendations)

---

## Project Structure

```
test_automation/
├── conftest.py                  # PyTest fixtures and browser setup
├── pages/                       # Page Object classes
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── profile_page.py
│   └── registration_page.py
├── tests/
│   └── test_application.py      # Test cases mapped from manual specs
├── utils/
│   └── data.py                  # Test data for parameterization
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Chrome or Mozilla Firefox installed
- ChromeDriver or GeckoDriver available in PATH

### Installation

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd test_automation
   ```

2. **Install dependencies:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure WebDriver (if needed):**
   - Make sure `chromedriver` or `geckodriver` is available in your PATH.
   - Download from:
     - ChromeDriver: https://chromedriver.chromium.org/downloads
     - GeckoDriver: https://github.com/mozilla/geckodriver/releases

4. **Set the base URL:**
   - Update the `BASE_URL` in `tests/test_application.py` to match your application's environment.

---

## Running Tests

### Run all tests (default: Chrome, headless):

```
pytest --browser=chrome --html=report.html
```

### Run with Firefox:

```
pytest --browser=firefox --html=report.html
```

### Run a single test case:

```
pytest tests/test_application.py::TestApplication::test_tc_001_verify_login_functionality
```

---

## Sample Test Results

Example output for a successful test run:

```
==================== test session starts ====================
collected 10 items

tests/test_application.py ..........                  [100%]

---------- generated html file: report.html ----------
===================== 10 passed in 45.21s ==================
```

- An HTML report will be generated as `report.html` for easy review.

---

## Troubleshooting

### Common Issues

- **WebDriverException:**
  - Ensure the correct driver (ChromeDriver/GeckoDriver) is installed and matches your browser version.
  - Check that the driver is in your system PATH.

- **TimeoutException:**
  - Check if the application under test is accessible and responsive.
  - Increase element wait times in `base_page.py` if necessary.

- **ModuleNotFoundError:**
  - Ensure you are running tests from the `test_automation/` root.
  - Activate your Python virtual environment.

### Environment Configuration

- You may set environment variables or use a `.env` file for sensitive data (credentials, endpoints).
- For CI/CD, pass the `--browser` flag and ensure drivers are available on build agents.

---

## Extending the Framework

- **Adding New Pages:**
  - Create a new page class in the `pages/` directory inheriting from `BasePage`.
  - Define locators and methods for new page interactions.

- **Adding New Tests:**
  - Add test methods to `tests/test_application.py` or create new test modules.

- **Parameterizing Tests:**
  - Use PyTest's `@pytest.mark.parametrize` for data-driven scenarios.

- **Selectors:**
  - Update placeholder locators in page objects to match your application's HTML.

---

## Best Practices & Recommendations

- Keep locators up to date and prefer unique IDs or data attributes.
- Use explicit waits (`WebDriverWait`) for robust synchronization.
- Modularize page actions and assertions for reuse.
- Review test data in `utils/data.py` for real-world coverage.
- Integrate with CI/CD for continuous validation (e.g., GitHub Actions, Jenkins).
- Regularly update dependencies in `requirements.txt`.

---

## Support & Feedback

For issues, suggestions, or contributions, please open a GitHub issue or contact the QA automation team.

#
# Below is the full Python code for the test automation suite as described above.
#

# conftest.py
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")

@pytest.fixture(scope="session")
def browser(request):
    """Fixture to initialize and quit browser instance."""
    browser_choice = request.config.getoption("--browser")
    if browser_choice.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser_choice.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_choice}")

    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator):
        """Wait for element to be present and return it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Wait for element to be clickable and click it."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def send_keys(self, locator, keys):
        """Wait for element and send keys."""
        element = self.find(locator)
        element.clear()
        element.send_keys(keys)

    def is_visible(self, locator):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def get_text(self, locator):
        """Get text of an element."""
        element = self.find(locator)
        return element.text

    def wait_until_url_contains(self, fragment):
        """Wait until the URL contains a fragment."""
        WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(fragment)
        )

# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page object for the login page."""

    # Placeholder locators - replace with actual selectors as needed
    USERNAME_INPUT = (By.ID, "login-username")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    BLANK_FIELDS_ERROR = (By.XPATH, "//div[contains(text(), 'Fields cannot be blank')]")

    def load(self, base_url):
        self.driver.get(f"{base_url}/login")

    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)

    def is_login_error_displayed(self, message=None):
        if message:
            try:
                return message in self.get_text(self.ERROR_MESSAGE)
            except:
                return False
        return self.is_visible(self.ERROR_MESSAGE)

    def is_blank_fields_error_displayed(self):
        return self.is_visible(self.BLANK_FIELDS_ERROR)

# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """Page object for the dashboard."""

    # Placeholder locators - update as per actual application
    DASHBOARD_URL_FRAGMENT = "/dashboard"
    WIDGETS = (By.CSS_SELECTOR, ".dashboard-widget")
    LOGOUT_BUTTON = (By.ID, "logout-button")

    def is_loaded(self):
        return self.DASHBOARD_URL_FRAGMENT in self.driver.current_url

    def widgets_displayed(self):
        try:
            widgets = self.driver.find_elements(*self.WIDGETS)
            return len(widgets) > 0
        except:
            return False

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

# pages/profile_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProfilePage(BasePage):
    """Page object for user profile/settings."""

    # Placeholder locators
    PROFILE_URL_FRAGMENT = "/profile"
    PROFILE_MENU = (By.ID, "profile-menu")
    EDIT_BUTTON = (By.ID, "edit-profile")
    NAME_INPUT = (By.ID, "profile-name")
    EMAIL_INPUT = (By.ID, "profile-email")
    SAVE_BUTTON = (By.ID, "save-profile")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")

    def load(self, base_url):
        self.driver.get(f"{base_url}/profile")

    def update_profile(self, name, email):
        self.click(self.EDIT_BUTTON)
        self.send_keys(self.NAME_INPUT, name)
        self.send_keys(self.EMAIL_INPUT, email)
        self.click(self.SAVE_BUTTON)

    def is_update_successful(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

# pages/registration_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegistrationPage(BasePage):
    """Page object for the registration page."""

    # Placeholder locators
    REGISTRATION_URL_FRAGMENT = "/register"
    EMAIL_INPUT = (By.ID, "register-email")
    USERNAME_INPUT = (By.ID, "register-username")
    PASSWORD_INPUT = (By.ID, "register-password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "register-confirm-password")
    TERMS_CHECKBOX = (By.ID, "accept-terms")
    SUBMIT_BUTTON = (By.ID, "register-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    FIELD_ERROR = (By.CSS_SELECTOR, ".field-error")

    def load(self, base_url):
        self.driver.get(f"{base_url}/register")

    def register(self, username, email, password, confirm_password, accept_terms=True):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        if accept_terms:
            self.click(self.TERMS_CHECKBOX)
        self.click(self.SUBMIT_BUTTON)

    def is_error_displayed(self, message=None):
        if message:
            try:
                return message in self.get_text(self.ERROR_MESSAGE)
            except:
                return False
        return self.is_visible(self.ERROR_MESSAGE)

    def mandatory_field_errors_displayed(self):
        try:
            errors = self.driver.find_elements(*self.FIELD_ERROR)
            return len(errors) > 0
        except:
            return False

# utils/data.py
# Test data for parameterization (replace with actual data as needed)
VALID_USER = {"username": "testuser", "password": "TestPass123", "email": "testuser@example.com"}
INVALID_USER = {"username": "wronguser", "password": "WrongPass"}
PROFILE_UPDATE = {"name": "New Name", "email": "newemail@example.com"}
INVALID_EMAIL = "not-an-email"

# tests/test_application.py
import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from utils.data import VALID_USER, INVALID_USER, PROFILE_UPDATE, INVALID_EMAIL

BASE_URL = "http://localhost:8000"  # Replace with actual base URL

@pytest.mark.usefixtures("browser")
class TestApplication:

    def test_tc_001_verify_login_functionality(self, browser):
        """TC-001: Verify Login Functionality"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login(VALID_USER["username"], VALID_USER["password"])
        dashboard = DashboardPage(browser)
        assert dashboard.is_loaded(), "User is not redirected to dashboard"

    def test_tc_002_validate_password_reset(self, browser):
        """TC-002: Validate Password Reset"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.click_forgot_password()
        # Simulate entering registered email and submit
        email_input = (By.ID, "reset-email")
        submit_button = (By.ID, "reset-submit")
        login_page.send_keys(email_input, VALID_USER["email"])
        login_page.click(submit_button)
        # Placeholder: Verify success message or email sent indication
        assert login_page.is_visible((By.CSS_SELECTOR, ".reset-success")), \
            "Password reset link not sent to registered email"

    def test_tc_003_check_login_failure_invalid_credentials(self, browser):
        """TC-003: Check Login Failure for Invalid Credentials"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login(INVALID_USER["username"], INVALID_USER["password"])
        assert login_page.is_login_error_displayed("Invalid credentials"), \
            "Expected error message for invalid credentials not displayed"

    def test_tc_004_verify_dashboard_widgets_display(self, browser):
        """TC-004: Verify Dashboard Widgets Display"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login(VALID_USER["username"], VALID_USER["password"])
        dashboard = DashboardPage(browser)
        assert dashboard.widgets_displayed(), "Dashboard widgets are not displayed correctly"

    def test_tc_005_check_logout_functionality(self, browser):
        """TC-005: Check Logout Functionality"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login(VALID_USER["username"], VALID_USER["password"])
        dashboard = DashboardPage(browser)
        dashboard.logout()
        login_page = LoginPage(browser)
        # Wait for login page to load
        assert "login" in browser.current_url, "User is not redirected to login page after logout"

    def test_tc_006_validate_profile_update(self, browser):
        """TC-006: Validate Profile Update"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login(VALID_USER["username"], VALID_USER["password"])
        profile = ProfilePage(browser)
        profile.load(BASE_URL)
        profile.update_profile(PROFILE_UPDATE["name"], PROFILE_UPDATE["email"])
        assert profile.is_update_successful(), "Profile update success message not displayed"

    def test_tc_007_check_error_message_blank_login_fields(self, browser):
        """TC-007: Check Error Message for Blank Login Fields"""
        login_page = LoginPage(browser)
        login_page.load(BASE_URL)
        login_page.login("", "")
        assert login_page.is_blank_fields_error_displayed(), \
            "Error message for blank fields is not displayed"

    def test_tc_008_verify_email_format_validation_registration(self, browser):
        """TC-008: Verify Email Format Validation on Registration"""
        registration_page = RegistrationPage(browser)
        registration_page.load(BASE_URL)
        registration_page.register(
            username="user1",
            email=INVALID_EMAIL,
            password="Password123",
            confirm_password="Password123"
        )
        assert registration_page.is_error_displayed("Invalid email format"), \
            "Error message for invalid email format is not displayed"

    def test_tc_009_check_mandatory_fields_validation_registration(self, browser):
        """TC-009: Check Mandatory Fields Validation on Registration"""
        registration_page = RegistrationPage(browser)
        registration_page.load(BASE_URL)
        registration_page.register(
            username="",
            email="",
            password="",
            confirm_password=""
        )
        assert registration_page.mandatory_field_errors_displayed(), \
            "Mandatory field error messages are not displayed"

    def test_tc_010_validate_terms_and_conditions_acceptance(self, browser):
        """TC-010: Validate Terms and Conditions Acceptance"""
        registration_page = RegistrationPage(browser)
        registration_page.load(BASE_URL)
        registration_page.register(
            username="user2",
            email="user2@example.com",
            password="Password123",
            confirm_password="Password123",
            accept_terms=False
        )
        assert registration_page.is_error_displayed("Please accept Terms and Conditions"), \
            "Error message for unaccepted Terms and Conditions not displayed"

# requirements.txt
selenium>=4.11.2
pytest>=7.4.0
pytest-html>=4.0.2
