# File: requirements.txt

selenium>=4.10.0
pytest>=7.0.0
pytest-html>=3.2.0

---

# File: config.py

"""
Framework configuration settings.
Modify as needed for target environment, browser, and test data.
"""

SELENIUM_DRIVER = "chrome"  # Supported: "chrome", "firefox"
BASE_URL = "https://example.com"  # Replace with actual application URL

# Placeholder credentials for testing
VALID_USERNAME = "testuser"
VALID_PASSWORD = "securepassword"
INVALID_USERNAME = "invaliduser"
INVALID_PASSWORD = "wrongpassword"
REGISTERED_EMAIL = "testuser@example.com"

# Timeout settings (seconds)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 10

---

# File: pages/login_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for Login Page.
    Encapsulates login page interactions.
    """
    URL = "/login"  # Path appended to BASE_URL

    # Locators (replace with actual selectors as needed)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self, base_url):
        self.driver.get(base_url + self.URL)
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except:
            return None

    def click_forgot_password(self):
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()

---

# File: pages/dashboard_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object Model for Dashboard Page.
    Validates dashboard presence after login.
    """
    DASHBOARD_IDENTIFIER = (By.ID, "dashboard-main")  # Placeholder selector

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.DASHBOARD_IDENTIFIER))
            return True
        except:
            return False

---

# File: pages/forgot_password_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotPasswordPage:
    """
    Page Object Model for Forgot Password Page.
    Handles password reset workflow.
    """
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_BUTTON = (By.ID, "submitBtn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def submit_email(self, email):
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT)).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)).text
        except:
            return None

---

# File: conftest.py

import pytest
from selenium import webdriver
from config import SELENIUM_DRIVER, IMPLICIT_WAIT

@pytest.fixture(scope="session")
def driver():
    """
    PyTest fixture to initialize and tear down Selenium WebDriver.
    Supports Chrome and Firefox.
    """
    if SELENIUM_DRIVER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Remove for headed mode
        driver = webdriver.Chrome(options=options)
    elif SELENIUM_DRIVER == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {SELENIUM_DRIVER}")

    driver.implicitly_wait(IMPLICIT_WAIT)
    yield driver
    driver.quit()

---

# File: tests/test_login.py

import pytest
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.high
def test_verify_login_functionality(driver):
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
    login_page.load(BASE_URL)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard not loaded after login"

@pytest.mark.high
def test_check_login_with_invalid_credentials(driver):
    """
    TC-003: Check Login with Invalid Credentials
    Preconditions: User account does not exist or password is incorrect
    Steps:
        1. Navigate to login page
        2. Enter invalid username and password
        3. Click login button
    Expected Result: Error message is displayed: 'Invalid credentials'
    """
    login_page = LoginPage(driver)
    login_page.load(BASE_URL)
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

    error_msg = login_page.get_error_message()
    assert error_msg is not None, "Error message not displayed for invalid login"
    assert "Invalid credentials" in error_msg, f"Unexpected error message: {error_msg}"

---

# File: tests/test_forgot_password.py

import pytest
from config import BASE_URL, REGISTERED_EMAIL
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage

@pytest.mark.medium
def test_validate_forgot_password_flow(driver):
    """
    TC-002: Validate Forgot Password Flow
    Preconditions: User account exists with valid email
    Steps:
        1. Navigate to login page
        2. Click 'Forgot Password' link
        3. Enter registered email
        4. Submit request
    Expected Result: Password reset email is sent
    """
    login_page = LoginPage(driver)
    login_page.load(BASE_URL)
    login_page.click_forgot_password()

    forgot_password_page = ForgotPasswordPage(driver)
    forgot_password_page.submit_email(REGISTERED_EMAIL)

    success_msg = forgot_password_page.get_success_message()
    assert success_msg is not None, "Success message not displayed for password reset"
    assert "Password reset email is sent" in success_msg or "Check your email" in success_msg, \
        f"Unexpected success message: {success_msg}"

---

# File: README.md

# Selenium + PyTest Automation Suite

## Overview

This project provides a modular, maintainable Selenium automation framework for validating login and password reset workflows, based on manual test cases extracted from Jira ticket SCRUM-6.

- **Framework:** Page Object Model (POM)
- **Test Runner:** PyTest
- **Browsers Supported:** Chrome, Firefox (headless by default)
- **Reporting:** PyTest HTML plugin

## Directory Structure

```
.
├── config.py
├── conftest.py
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── forgot_password_page.py
├── tests/
│   ├── test_login.py
│   └── test_forgot_password.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Install Python 3.8+** (recommended)
2. **Clone this repository** and navigate to its root directory.
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Download WebDriver binaries:**
   - [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)
   - Ensure the driver is in your system PATH.

5. **Configure environment:**
   - Edit `config.py` to set `BASE_URL` and test credentials.
   - Adjust `SELENIUM_DRIVER` for your browser.

## Running Tests

Execute all tests:
```
pytest --html=report.html
```

Run a specific test file:
```
pytest tests/test_login.py
```

## Sample Test Results

```
======================================= test session starts =======================================
collected 3 items

tests/test_login.py::test_verify_login_functionality       PASSED
tests/test_login.py::test_check_login_with_invalid_credentials  PASSED
tests/test_forgot_password.py::test_validate_forgot_password_flow PASSED

--------------------------------------- HTML report generated -------------------------------------
```

## Troubleshooting

- **WebDriverException:** Ensure ChromeDriver/GeckoDriver is installed and PATH is set.
- **ElementNotFound:** Update selectors in `pages/` if application UI changes.
- **Timeouts:** Adjust `IMPLICIT_WAIT` and `EXPLICIT_WAIT` in `config.py`.
- **Environment Issues:** Verify Python and pip versions, and that all dependencies are installed.

## Extending the Framework

- Add new page objects to `pages/`.
- Create new test modules in `tests/`.
- Use PyTest parameterization for data-driven scenarios.
- Integrate with CI/CD by running `pytest` and collecting the HTML report.

## Best Practices & Recommendations

- Keep selectors up-to-date with UI changes.
- Avoid hard-coded credentials in production.
- Use explicit waits for reliable synchronization.
- Modularize page objects for reuse.
- Regularly update dependencies and drivers.

## Feedback & Maintenance

- For bug reports or enhancement requests, update the test specification JSON or Excel and regenerate automation code.
- Review test execution logs and HTML reports for failures.
- Plan for framework upgrades with each application release.

---

# End of Final Answer
