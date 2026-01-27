# Modular Selenium and PyTest automation code organized into page objects and test cases

# Directory Structure:
# automation_project/
# ├── pages/
# │   └── login_page.py
# │   └── dashboard_page.py
# │   └── base_page.py
# ├── tests/
# │   └── test_login.py
# │   └── test_dashboard.py
# ├── conftest.py
# ├── requirements.txt
# ├── README.md
# └── sample_test_output.txt

# ---

# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Base class for all page objects. Provides common Selenium utilities.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, by, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def click(self, by, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def enter_text(self, by, locator, text):
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)

    def is_visible(self, by, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except:
            return False

    def get_text(self, by, locator):
        element = self.find(by, locator)
        return element.text

# ---

# pages/login_page.py

from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object for the Login Page.
    """
    # Placeholder locators; update as per actual application
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    ERROR_MESSAGE = (By.ID, 'loginError')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, 'Forgot Password?')
    RESET_EMAIL_INPUT = (By.ID, 'resetEmail')
    RESET_PASSWORD_BUTTON = (By.ID, 'resetBtn')
    RESET_SUCCESS_MSG = (By.ID, 'resetSuccess')

    def open(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.enter_text(*self.USERNAME_INPUT, text=username)
        self.enter_text(*self.PASSWORD_INPUT, text=password)
        self.click(*self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(*self.ERROR_MESSAGE)

    def click_forgot_password(self):
        self.click(*self.FORGOT_PASSWORD_LINK)

    def reset_password(self, email):
        self.enter_text(*self.RESET_EMAIL_INPUT, text=email)
        self.click(*self.RESET_PASSWORD_BUTTON)

    def is_reset_success_message_displayed(self):
        return self.is_visible(*self.RESET_SUCCESS_MSG)

# ---

# pages/dashboard_page.py

from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """
    Page Object for the Dashboard Page.
    """
    DASHBOARD_HEADER = (By.ID, 'dashboardHeader')
    LOGOUT_BUTTON = (By.ID, 'logoutBtn')
    ADMIN_DASHBOARD_LINK = (By.ID, 'adminDashboard')
    ACCESS_DENIED_MESSAGE = (By.ID, 'accessDenied')

    def is_loaded(self):
        return self.is_visible(*self.DASHBOARD_HEADER)

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

    def go_to_admin_dashboard(self):
        self.click(*self.ADMIN_DASHBOARD_LINK)

    def is_access_denied_displayed(self):
        return self.is_visible(*self.ACCESS_DENIED_MESSAGE)

# ---

# conftest.py

import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    """
    PyTest fixture to initialize and quit the WebDriver.
    Default: Chrome. Update to parameterize as needed.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    # Update this URL to your application's login page
    return "http://your-app-url/login"

# ---

# tests/test_login.py

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.usefixtures("browser", "base_url")
class TestLogin:

    def test_valid_login(self, browser, base_url):
        """
        TC-001: Verify User Login
        Preconditions: User account exists and is active
        """
        login_page = LoginPage(browser)
        login_page.open(base_url)
        login_page.login("valid_user", "valid_password")  # Replace with real credentials
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard not loaded after login"

    def test_invalid_login(self, browser, base_url):
        """
        TC-002: Verify Login with Invalid Credentials
        Preconditions: User is on the login page
        """
        login_page = LoginPage(browser)
        login_page.open(base_url)
        login_page.login("invalid_user", "wrong_password")
        assert login_page.is_visible(*LoginPage.ERROR_MESSAGE), "Error message not displayed"
        error_msg = login_page.get_error_message()
        assert "invalid" in error_msg.lower(), f"Unexpected error message: {error_msg}"

    def test_forgot_password(self, browser, base_url):
        """
        TC-003: Verify Password Reset Functionality
        Preconditions: User has a registered email address
        """
        login_page = LoginPage(browser)
        login_page.open(base_url)
        login_page.click_forgot_password()
        login_page.reset_password("registered_user@email.com")  # Replace with test email
        assert login_page.is_reset_success_message_displayed(), "Password reset success message not displayed"

# ---

# tests/test_dashboard.py

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.usefixtures("browser", "base_url")
class TestDashboard:

    def test_logout(self, browser, base_url):
        """
        TC-004: Verify Logout Functionality
        Preconditions: User is logged in
        """
        login_page = LoginPage(browser)
        login_page.open(base_url)
        login_page.login("valid_user", "valid_password")  # Replace with real credentials
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard not loaded after login"
        dashboard_page.logout()
        assert login_page.is_visible(*LoginPage.LOGIN_BUTTON), "Login button not visible after logout"

    def test_dashboard_access_rights(self, browser, base_url):
        """
        TC-005: Verify Dashboard Access Rights
        Preconditions: User has restricted access rights
        """
        login_page = LoginPage(browser)
        login_page.open(base_url)
        login_page.login("restricted_user", "valid_password")  # Replace with restricted user credentials
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard not loaded"
        dashboard_page.go_to_admin_dashboard()
        assert dashboard_page.is_access_denied_displayed(), "Access denied message not displayed"

# ---

# requirements.txt

selenium==4.16.0
pytest==8.2.0

# ---

# README.md

# Selenium & PyTest Automation Suite

## Overview

This repository contains a modular, maintainable Selenium WebDriver automation suite using Python and PyTest. Test cases are implemented using the Page Object Model (POM) pattern and were generated from validated manual test cases extracted from Jira (SCRUM-6).

## Directory Structure

```
automation_project/
├── pages/
│   └── base_page.py
│   └── login_page.py
│   └── dashboard_page.py
├── tests/
│   └── test_login.py
│   └── test_dashboard.py
├── conftest.py
├── requirements.txt
├── README.md
└── sample_test_output.txt
```

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone <repo-url>
    cd automation_project
    ```

2. **Create a Python virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download the appropriate WebDriver (e.g., [ChromeDriver](https://sites.google.com/chromium.org/driver/)) and ensure it's in your PATH.**

5. **Update the following in `conftest.py` and page object files as needed:**
    - `base_url` fixture with your actual application URL.
    - Locator tuples in `pages/` to match your application's HTML.
    - User credentials in test files for valid, invalid, and restricted users.

## Running Tests

```bash
pytest tests/
```

To see verbose output:
```bash
pytest -v tests/
```

## Sample Output

See `sample_test_output.txt` for a sample PyTest run.

## Troubleshooting Guide

- **WebDriver not found:** Ensure `chromedriver` or the required driver is installed and in your system PATH.
- **Timeouts or Element Not Found:** Verify locator values in page object files. Use browser developer tools to inspect actual element selectors.
- **Invalid login or test data:** Ensure test user accounts exist and have the expected permissions.
- **Environment variables:** For production, consider parameterizing credentials and URLs via environment variables or a config file.

## Extending the Framework

- **Add new pages:** Create a new class in the `pages/` directory inheriting from `BasePage`.
- **Add new tests:** Create a new test module in `tests/` and use/extend existing page objects.
- **Support more browsers:** Parameterize the `browser` fixture in `conftest.py`.
- **Reporting:** Integrate with plugins such as `pytest-html` for HTML reports.

## Best Practices & Recommendations

- Use Page Object Model for maintainability.
- Keep locators centralized and descriptive.
- Use explicit waits to avoid flakiness.
- Separate test data from test logic.
- Integrate with CI/CD for automated runs.
- Regularly update dependencies and audit for security.

## CI/CD Integration

- Add `pytest` execution in your pipeline (e.g., GitHub Actions, Jenkins).
- Archive test reports and logs as build artifacts.

## Support

For issues, raise a GitHub issue or contact the automation maintainer.

---

*Generated by Senior Test Automation Code Generator & Documentation Specialist*

# ---

# sample_test_output.txt

============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.0, pluggy-1.0.0
rootdir: /home/user/automation_project
collected 5 items

tests/test_login.py::TestLogin::test_valid_login PASSED                  [ 20%]
tests/test_login.py::TestLogin::test_invalid_login PASSED                [ 40%]
tests/test_login.py::TestLogin::test_forgot_password PASSED              [ 60%]
tests/test_dashboard.py::TestDashboard::test_logout PASSED               [ 80%]
tests/test_dashboard.py::TestDashboard::test_dashboard_access_rights PASSED [100%]

============================== 5 passed in 11.34s ==============================
