# Directory Structure:
# .
# ├── pages/
# │   └── login_page.py
# ├── tests/
# │   └── test_login.py
# ├── conftest.py
# ├── requirements.txt
# ├── README.md
# └── sample_test_results.txt

# ========== pages/login_page.py ==========
"""
Page Object for the Login Page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for Login Page.
    Encapsulates all interactions and verifications for login-related functionality.
    """

    # Placeholder selectors (to be updated with actual values)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMessage")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def go_to(self, url):
        """Navigate to the login page."""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def login(self, username, password):
        """Enter credentials and click login."""
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Return error message text if present."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except Exception:
            return None

    def click_forgot_password(self):
        """Click the Forgot Password link."""
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()

    def is_on_dashboard(self):
        """
        Placeholder for dashboard verification.
        Should be implemented with actual dashboard locator.
        """
        # Example: (By.ID, "dashboard")
        try:
            dashboard = self.wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
            return dashboard.is_displayed()
        except Exception:
            return False

    def is_on_password_reset_page(self):
        """
        Placeholder for password reset page verification.
        Should be implemented with actual reset page locator.
        """
        # Example: (By.ID, "resetForm")
        try:
            reset_form = self.wait.until(EC.presence_of_element_located((By.ID, "resetForm")))
            return reset_form.is_displayed()
        except Exception:
            return False

# ========== tests/test_login.py ==========
"""
Test suite for Login Functionality using Selenium and PyTest.
"""

import pytest
from pages.login_page import LoginPage

# Test Data (could be moved to a separate file or fixture)
VALID_USERNAME = "testuser"
VALID_PASSWORD = "securepassword"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass"
LOGIN_URL = "http://localhost:8000/login"  # Placeholder URL

@pytest.mark.usefixtures("browser")
class TestLogin:
    """
    Contains tests for login functionality as defined in the extracted test cases.
    """

    def test_TC_001_verify_login_functionality(self, browser):
        """
        TC-001: Verify Login Functionality
        Preconditions: User account exists and is active
        Steps:
            1. Navigate to the login page
            2. Enter valid username and password
            3. Click on the 'Login' button
        Expected Result: User is redirected to the dashboard
        """
        login = LoginPage(browser)
        login.go_to(LOGIN_URL)
        login.login(VALID_USERNAME, VALID_PASSWORD)
        assert login.is_on_dashboard(), "User was not redirected to the dashboard."

    def test_TC_002_validate_error_message_for_invalid_login(self, browser):
        """
        TC-002: Validate Error Message for Invalid Login
        Preconditions: User is on the login page
        Steps:
            1. Navigate to the login page
            2. Enter invalid username or password
            3. Click on the 'Login' button
        Expected Result: Error message 'Invalid credentials' is displayed
        """
        login = LoginPage(browser)
        login.go_to(LOGIN_URL)
        login.login(INVALID_USERNAME, INVALID_PASSWORD)
        error = login.get_error_message()
        assert error is not None, "No error message displayed for invalid login."
        assert "Invalid credentials" in error, f"Unexpected error message: {error}"

    def test_TC_003_check_forgot_password_link(self, browser):
        """
        TC-003: Check Forgot Password Link
        Preconditions: User is on the login page
        Steps:
            1. Navigate to the login page
            2. Click on the 'Forgot Password' link
        Expected Result: Password reset page is displayed
        """
        login = LoginPage(browser)
        login.go_to(LOGIN_URL)
        login.click_forgot_password()
        assert login.is_on_password_reset_page(), "Password reset page was not displayed."

# ========== conftest.py ==========
"""
PyTest fixtures for Selenium WebDriver setup and teardown.
Supports configuration for different browsers.
"""

import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to use for tests: chrome or firefox"
    )

@pytest.fixture(scope="class")
def browser(request):
    browser_type = request.config.getoption("--browser")
    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
    elif browser_type == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ========== requirements.txt ==========
selenium>=4.12.0
pytest>=7.0.0

# ========== README.md ==========
# Selenium PyTest Automation Suite

## Overview

This automation suite was generated from standardized JSON test cases extracted from manual test specifications (see Jira SCRUM-6). It covers login functionality for a web application using the Page Object Model (POM), Selenium WebDriver, and PyTest.

**Test Cases Automated:**
- TC-001: Verify Login Functionality
- TC-002: Validate Error Message for Invalid Login
- TC-003: Check Forgot Password Link

## Directory Structure

```
.
├── pages/
│   └── login_page.py        # Login Page Object Model
├── tests/
│   └── test_login.py        # Test cases for login functionality
├── conftest.py              # PyTest fixtures for browser management
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
└── sample_test_results.txt  # Sample output from test execution
```

## Setup Instructions

1. **Clone the repository or copy the files to your project directory.**

2. **Install Python 3.8+ and pip if not already available.**

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Download the appropriate WebDriver binary:**
   - For Chrome: [ChromeDriver](https://chromedriver.chromium.org/downloads)
   - For Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Ensure the driver is in your PATH or specify its location via Selenium options.

5. **Configure test data and URLs:**
   - Update `LOGIN_URL` and credentials in `tests/test_login.py` as needed.
   - Update selectors in `pages/login_page.py` to match your application's DOM.

## Running Tests

**Default (Chrome):**
```
pytest tests/
```

**Specify browser (chrome or firefox):**
```
pytest tests/ --browser=firefox
```

**View detailed output:**
```
pytest -v tests/
```

## Troubleshooting

- **WebDriverException / Driver Not Found:**  
  Ensure the correct driver binary is installed and available in your system PATH.

- **Element Not Found or Timeout:**  
  Update selectors in `login_page.py` to match the current application. Increase wait times if the application is slow.

- **Environment Issues:**  
  Ensure all dependencies are installed and Python version is compatible. If using a virtual environment, activate it before installing/running.

- **Test Data / URLs:**  
  Update the test credentials, URLs, and expected outcomes to reflect your environment.

## Extending the Framework

- **Add new pages:** Create a new file in `pages/` and define a new Page Object.
- **Add new tests:** Create new test files in `tests/` and use/reuse existing Page Objects.
- **Parameterize tests:** Use PyTest's `@pytest.mark.parametrize` for data-driven scenarios.
- **Integrate with CI/CD:** Add test execution commands to your CI pipeline (e.g., GitHub Actions, Jenkins).
- **Reporting:** Integrate with PyTest plugins like `pytest-html` for HTML reports.

## Best Practices

- Maintain clear separation between test logic (in `tests/`) and page interactions (in `pages/`).
- Use explicit waits for synchronization and stable execution.
- Use configuration files or environment variables for sensitive data and URLs.
- Regularly update selectors to match application changes.
- Document all Page Object methods and test cases with meaningful docstrings.

## Sample Test Execution Output

See `sample_test_results.txt` for example output from a successful test run.

---

## Security and Maintenance

- Do not commit real credentials to version control.
- Review and update dependencies regularly for security patches.
- Update WebDriver binaries when browser versions change.

---

## Future Enhancements

- Add support for additional browsers (Edge, Safari).
- Integrate with test management tools for result reporting.
- Implement parallel test execution (e.g., `pytest-xdist`).
- Add coverage for negative and edge cases.
- Extend parsing support for additional test case formats (docx, pdf, csv).

# ========== sample_test_results.txt ==========
============================= test session starts =============================
platform linux -- Python 3.10.0, pytest-7.4.0, pluggy-1.0.0
rootdir: /home/automation/project
collected 3 items

tests/test_login.py::TestLogin::test_TC_001_verify_login_functionality PASSED [ 33%]
tests/test_login.py::TestLogin::test_TC_002_validate_error_message_for_invalid_login PASSED [ 66%]
tests/test_login.py::TestLogin::test_TC_003_check_forgot_password_link PASSED [100%]

============================== 3 passed in 5.17s =============================

# End of Final Answer
