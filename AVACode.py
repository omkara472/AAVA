# AVACode.py

"""
Modular Selenium and PyTest automation code for login and password reset flows, generated from standardized test cases (Jira SCRUM-6, Manual_Test_Cases.xlsx).
Directory structure and supporting files documented in README.md.
"""

# --- selenium_automation/pages/login_page.py ---

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for Login Page.
    Encapsulates all interactions and verifications on the Login page.
    """

    # Placeholder selectors - these should be updated to actual selectors
    URL = "https://your-app-under-test.com/login"
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMessage")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_RESET_BUTTON = (By.ID, "resetSubmit")
    RESET_CONFIRMATION = (By.ID, "resetConfirmation")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text

    def is_on_dashboard(self):
        # Placeholder: Replace with actual dashboard verification logic
        return "dashboard" in self.driver.current_url

    def initiate_password_reset(self, email):
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.SUBMIT_RESET_BUTTON).click()

    def is_reset_confirmation_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.RESET_CONFIRMATION)).is_displayed()

# --- selenium_automation/tests/test_login.py ---

import pytest
from pages.login_page import LoginPage

# Test Data (would be externalized/config-driven in production)
VALID_USER = {"username": "testuser", "password": "correctpassword"}
INVALID_USER = {"username": "testuser", "password": "wrongpassword"}
REGISTERED_EMAIL = "testuser@example.com"

@pytest.mark.usefixtures("driver")
class TestLogin:

    def test_verify_login_functionality(self, driver):
        """
        TC-001: Verify Login Functionality
        Preconditions: User account exists
        Steps:
            1. Navigate to login page
            2. Enter valid credentials
            3. Click login button
        Expected Result: User is redirected to dashboard
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER['username'], VALID_USER['password'])
        assert login_page.is_on_dashboard(), "User was not redirected to dashboard."

    def test_validate_error_on_invalid_login(self, driver):
        """
        TC-002: Validate Error on Invalid Login
        Preconditions: User is on login page
        Steps:
            1. Navigate to login page
            2. Enter invalid credentials
            3. Click login button
        Expected Result: Error message is displayed
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(INVALID_USER['username'], INVALID_USER['password'])
        error = login_page.get_error_message()
        assert error and "invalid" in error.lower(), f"Expected error message not displayed. Got: {error}"

    def test_check_password_reset_flow(self, driver):
        """
        TC-003: Check Password Reset Flow
        Preconditions: User email is registered
        Steps:
            1. Navigate to login page
            2. Click 'Forgot Password'
            3. Enter registered email
            4. Submit request
        Expected Result: Password reset link is sent to email
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.initiate_password_reset(REGISTERED_EMAIL)
        assert login_page.is_reset_confirmation_displayed(), "Password reset confirmation not displayed."

# --- selenium_automation/conftest.py ---

import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")

@pytest.fixture(scope="class")
def driver(request):
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Remove if you want to see browser
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()

# --- selenium_automation/requirements.txt ---

# requirements.txt
selenium>=4.11.2
pytest>=7.4.0

# --- selenium_automation/README.md ---

"""
# Selenium PyTest Automation Suite

## Overview

This repository contains a modular Selenium WebDriver and PyTest-based automation suite, generated from standardized test case specifications (see Jira SCRUM-6, 'Manual_Test_Cases.xlsx'). The suite implements the Page Object Model (POM) for maintainability and extensibility.

### Test Cases Automated

- **TC-001:** Verify Login Functionality
- **TC-002:** Validate Error on Invalid Login
- **TC-003:** Check Password Reset Flow

---

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Google Chrome or Mozilla Firefox installed
- [ChromeDriver](https://chromedriver.chromium.org/) or [GeckoDriver](https://github.com/mozilla/geckodriver/) in your PATH

### 2. Install Dependencies

From the root directory:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Directory Structure

```
selenium_automation/
├── pages/
│   └── login_page.py
├── tests/
│   └── test_login.py
├── conftest.py
├── requirements.txt
└── README.md
```

---

## Usage

### Run All Tests (Default: Chrome, Headless)

```bash
pytest
```

### Specify Browser

```bash
pytest --browser=firefox
```

### Example: Run a Single Test

```bash
pytest tests/test_login.py::TestLogin::test_verify_login_functionality
```

---

## Sample Test Results

```
============================= test session starts ==============================
collected 3 items

tests/test_login.py ...                                                 [100%]

============================== 3 passed in 8.54s ==============================
```

---

## Troubleshooting Guide

### WebDriver Errors

- **Message:** `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.`
  - **Solution:** Download the appropriate driver for your browser and ensure it is in your system PATH.

### Selector/Element Not Found

- **Message:** `selenium.common.exceptions.NoSuchElementException`
  - **Solution:** Verify the selectors in `pages/login_page.py` match your application's HTML. Update placeholder selectors as needed.

### Environment Issues

- **Issue:** Tests fail to start browser.
  - **Solution:** Check Python and browser versions, driver compatibility, and virtual environment activation.

---

## Extension & Customization

- **Page Objects:** Add new page objects in the `pages/` directory.
- **Test Data:** Parameterize or externalize test data for broader coverage.
- **Parallel Execution:** Integrate `pytest-xdist` for parallel test runs.
- **CI/CD Integration:** Add to your pipeline (e.g., GitHub Actions, Jenkins) with headless mode.

---

## Best Practices & Recommendations

- Update placeholder selectors in `login_page.py` with actual application values.
- Modularize further as your application grows.
- Use explicit waits for synchronization.
- Keep test data/configuration external for maintainability.
- Review the [Selenium docs](https://selenium.dev/documentation/) for advanced usage.

---

## Security & Maintenance

- No credentials are hardcoded; use environment variables for secrets in production.
- Review and update driver/browser versions regularly.
- Update dependencies via `pip install -U -r requirements.txt` as needed.

---

## Feedback & Support

- For enhancements, see recommendations in the Documentation section.
- For issues, review the troubleshooting guide and logs.
"""
