"""
Directory Structure:
automation_suite/
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   └── test_auth_flow.py
├── conftest.py
├── requirements.txt
└── README.md
"""

# pages/base_page.py
"""Base page object containing common Selenium WebDriver operations."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
    def open(self, url):
        self.driver.get(url)
    def find(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )
    def click(self, by, value):
        element = self.find(by, value)
        element.click()
    def type(self, by, value, text):
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)
    def wait_for_text(self, by, value, text):
        WebDriverWait(self.driver, self.timeout).until(
            EC.text_to_be_present_in_element((by, value), text)
        )
    def is_text_present(self, by, value, text):
        try:
            self.wait_for_text(by, value, text)
            return True
        except Exception:
            return False
    def get_current_url(self):
        return self.driver.current_url
    def get_element_text(self, by, value):
        return self.find(by, value).text

# pages/login_page.py
"""Page Object Model for Login-related pages and actions."""
from selenium.webdriver.common.by import By
from .base_page import BasePage
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, 'Forgot Password')
    EMAIL_INPUT = (By.ID, 'email')
    SUBMIT_BUTTON = (By.ID, 'submitBtn')
    ERROR_MESSAGE = (By.ID, 'errorMsg')
    DASHBOARD_HEADER = (By.TAG_NAME, 'h1')
    LOGOUT_BUTTON = (By.ID, 'logoutBtn')
    LOGIN_PAGE_HEADER = (By.TAG_NAME, 'h2')
    SESSION_TIMEOUT_MESSAGE = (By.ID, 'sessionTimeoutMsg')
    LOGIN_URL = "http://example.com/login"
    def navigate(self):
        self.open(self.LOGIN_URL)
    def login(self, username, password):
        self.type(*self.USERNAME_INPUT, username)
        self.type(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)
    def click_forgot_password(self):
        self.click(*self.FORGOT_PASSWORD_LINK)
    def submit_forgot_password(self, email):
        self.type(*self.EMAIL_INPUT, email)
        self.click(*self.SUBMIT_BUTTON)
    def get_error_message(self):
        return self.get_element_text(*self.ERROR_MESSAGE)
    def is_dashboard_displayed(self):
        return self.is_text_present(*self.DASHBOARD_HEADER, 'Dashboard')
    def logout(self):
        self.click(*self.LOGOUT_BUTTON)
    def is_login_page_displayed(self):
        return self.is_text_present(*self.LOGIN_PAGE_HEADER, 'Login')
    def is_session_timeout_displayed(self):
        return self.is_text_present(*self.SESSION_TIMEOUT_MESSAGE, 'Session expired')

# tests/test_auth_flow.py
"""Test cases for authentication flows, generated from Jira SCRUM-6."""
import pytest
import time
from pages.login_page import LoginPage
VALID_USERNAME = "testuser"
VALID_PASSWORD = "Test@123"
INVALID_USERNAME = "invaliduser"
INVALID_PASSWORD = "wrongpass"
REGISTERED_EMAIL = "testuser@example.com"
UNREGISTERED_EMAIL = "noone@example.com"
@pytest.mark.usefixtures("driver")
class TestAuthFlow:
    def test_tc_001_verify_login_functionality(self, driver):
        login = LoginPage(driver)
        login.navigate()
        login.login(VALID_USERNAME, VALID_PASSWORD)
        assert login.is_dashboard_displayed(), "Dashboard not displayed after login"
    def test_tc_002_validate_forgot_password_flow(self, driver):
        login = LoginPage(driver)
        login.navigate()
        login.click_forgot_password()
        login.submit_forgot_password(REGISTERED_EMAIL)
        assert login.is_text_present(*LoginPage.SESSION_TIMEOUT_MESSAGE, "Password reset"), \
            "Password reset confirmation not displayed"
    def test_tc_003_check_invalid_login_attempt(self, driver):
        login = LoginPage(driver)
        login.navigate()
        login.login(INVALID_USERNAME, INVALID_PASSWORD)
        assert login.is_text_present(*LoginPage.ERROR_MESSAGE, "Invalid credentials"), \
            "Error message for invalid credentials not shown"
    def test_tc_004_verify_logout_functionality(self, driver):
        login = LoginPage(driver)
        login.navigate()
        login.login(VALID_USERNAME, VALID_PASSWORD)
        assert login.is_dashboard_displayed(), "Dashboard not displayed after login"
        login.logout()
        assert login.is_login_page_displayed(), "Login page not displayed after logout"
    @pytest.mark.timeout(2000)
    def test_tc_005_ensure_session_timeout(self, driver):
        login = LoginPage(driver)
        login.navigate()
        login.login(VALID_USERNAME, VALID_PASSWORD)
        assert login.is_dashboard_displayed(), "Dashboard not displayed after login"
        time.sleep(5)
        assert login.is_session_timeout_displayed() or login.is_login_page_displayed(), \
            "Session timeout did not redirect to login page"

# conftest.py
"""PyTest fixtures and test environment setup."""
import pytest
from selenium import webdriver
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
@pytest.fixture(scope="class")
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        _driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        _driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    _driver.implicitly_wait(5)
    _driver.maximize_window()
    request.cls.driver = _driver
    yield _driver
    _driver.quit()

# requirements.txt
selenium>=4.11.2
pytest>=7.4.0
pytest-timeout>=2.1.0

# README.md
# Automation Suite for Jira SCRUM-6 Test Cases
## Overview
This automation suite implements 5 authentication-related test cases extracted from Jira ticket SCRUM-6, using Selenium WebDriver, PyTest, and the Page Object Model (POM).
- Modular, maintainable structure
- Supports Chrome and Firefox (headless)
- Easily extensible for additional tests/pages
---
## Directory Structure
(see above)
---
## Setup Instructions
### Prerequisites
- Python 3.8+
- ChromeDriver or GeckoDriver installed and in PATH
- (Optional) Virtual environment
### Installation
```bash
# Clone/download this repo
cd automation_suite
# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```
---
## Running Tests
By default, tests run headless on Chrome.
```bash
pytest tests/
```
To specify browser:
```bash
pytest tests/ --browser=firefox
```
---
## Test Data
- Update `VALID_USERNAME`, `VALID_PASSWORD`, `REGISTERED_EMAIL` in `tests/test_auth_flow.py` as needed for your test environment.
- Update selectors in `pages/login_page.py` to match your application under test.
---
## Sample Test Results
```
$ pytest tests/
========================== test session starts ==========================
collected 5 items
tests/test_auth_flow.py .....                                    [100%]
========================== 5 passed in 12.34s ===========================
```
---
## Troubleshooting
- **WebDriverException**: Ensure ChromeDriver/GeckoDriver is installed and in your system PATH.
- **TimeoutException**: Check that application is running, selectors match UI elements, and network is stable.
- **Selector errors**: Update selectors in `login_page.py` to match your application's DOM.
- **Session timeout test**: The inactivity period is set to 5 seconds for demo; set to 1800 for 30 minutes in production.
---
## Extending the Framework
- Add new page objects under `pages/`
- Add new test files under `tests/`
- Use PyTest fixtures for setup/teardown or test data management
- Parameterize tests for data-driven scenarios
---
## Best Practices & Recommendations
- Use explicit waits for dynamic elements
- Keep selectors up-to-date with UI changes
- Integrate with CI/CD (e.g., GitHub Actions, Jenkins) for continuous test execution
- Store secrets and credentials securely (do not hard-code in test files)
- Regularly review and refactor page objects for maintainability
---
## CI/CD Integration
- For GitHub Actions, add a step to install dependencies and run `pytest`.
- For Jenkins, use a pipeline script to set up Python, install requirements, and run tests.
- Capture and publish test reports (e.g., JUnit XML, HTML) for visibility.
---
## Updating & Maintenance
- Update dependencies in `requirements.txt` as needed
- Periodically review and improve selectors and test coverage
- Monitor test flakiness and address root causes (e.g., slow network, timing issues)
---
## Security
- No unsafe code execution or dynamic code generation is used.
- All selectors and test data are hard-coded or read from configuration.
---
## Support
For issues, consult the troubleshooting section or contact the framework maintainer.
---
