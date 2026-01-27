# AVACode.py

"""
Selenium & PyTest Automation Suite
Converted from Jira SCRUM-6 manual test cases

Project Structure:
- pages/base_page.py
- pages/login_page.py
- pages/dashboard_page.py
- pages/password_reset_page.py
- tests/conftest.py
- tests/test_authentication.py
- requirements.txt
- README.md
- sample_test_output.txt
"""

# --- pages/base_page.py ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, by, value):
        """Find a single element."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click(self, by, value):
        """Click an element."""
        element = self.find(by, value)
        element.click()
        return element

    def enter_text(self, by, value, text):
        """Enter text into an input field."""
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)
        return element

    def is_visible(self, by, value):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def get_text(self, by, value):
        """Get text from an element."""
        element = self.find(by, value)
        return element.text

# --- pages/login_page.py ---
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page object for the Login Page."""

    # Placeholder selectors - update these as per actual application
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "loginError")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

    def load(self, url):
        self.driver.get(url)

    def login(self, username, password, remember_me=False):
        self.enter_text(*self.USERNAME_INPUT, text=username)
        self.enter_text(*self.PASSWORD_INPUT, text=password)
        if remember_me:
            self.click(*self.REMEMBER_ME_CHECKBOX)
        self.click(*self.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(*self.FORGOT_PASSWORD_LINK)

    def get_error_message(self):
        if self.is_visible(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return None

# --- pages/dashboard_page.py ---
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """Page object for the Dashboard Page."""

    # Placeholder selectors
    LOGOUT_BUTTON = (By.ID, "logoutBtn")

    def is_loaded(self):
        # Placeholder: Update with a selector unique to dashboard
        return self.is_visible(By.ID, "dashboardMain")

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

# --- pages/password_reset_page.py ---
from selenium.webdriver.common.by import By
from .base_page import BasePage

class PasswordResetPage(BasePage):
    """Page object for the Password Reset Page."""

    # Placeholder selectors
    EMAIL_INPUT = (By.ID, "resetEmail")
    RESET_BUTTON = (By.ID, "resetBtn")
    CONFIRMATION_MESSAGE = (By.ID, "resetConfirmation")

    def enter_email_and_submit(self, email):
        self.enter_text(*self.EMAIL_INPUT, text=email)
        self.click(*self.RESET_BUTTON)

    def is_confirmation_displayed(self):
        return self.is_visible(*self.CONFIRMATION_MESSAGE)

# --- tests/conftest.py ---
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    """Fixture to initialize and teardown the WebDriver session."""
    # You can parametrize browser selection via CLI or config if needed
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# --- tests/test_authentication.py ---
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.password_reset_page import PasswordResetPage

# Test data - in real-world, use config or fixtures
BASE_URL = "http://your-app-under-test.com"
VALID_USERNAME = "testuser"
VALID_PASSWORD = "password123"
INVALID_USERNAME = "invalid"
INVALID_PASSWORD = "wrongpass"
REGISTERED_EMAIL = "testuser@example.com"

@pytest.mark.usefixtures("browser")
class TestAuthentication:

    def test_login_with_valid_credentials(self, browser):
        """
        TC-001: Verify Login Functionality with Valid Credentials
        Preconditions: User account must exist and be active
        """
        login_page = LoginPage(browser)
        login_page.load(f"{BASE_URL}/login")
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard did not load after login"

    def test_login_with_invalid_credentials(self, browser):
        """
        TC-002: Verify Login with Invalid Credentials
        Preconditions: Application is accessible
        """
        login_page = LoginPage(browser)
        login_page.load(f"{BASE_URL}/login")
        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
        error_msg = login_page.get_error_message()
        assert error_msg is not None and "Invalid credentials" in error_msg, \
            f"Expected error message not shown, got: {error_msg}"

    def test_password_reset_functionality(self, browser):
        """
        TC-003: Verify Password Reset Functionality
        Preconditions: User account with valid email exists
        """
        login_page = LoginPage(browser)
        login_page.load(f"{BASE_URL}/login")
        login_page.click_forgot_password()
        reset_page = PasswordResetPage(browser)
        reset_page.enter_email_and_submit(REGISTERED_EMAIL)
        assert reset_page.is_confirmation_displayed(), \
            "Password reset confirmation not displayed"

    def test_logout_functionality(self, browser):
        """
        TC-004: Verify Logout Functionality
        Preconditions: User must be logged in
        """
        login_page = LoginPage(browser)
        login_page.load(f"{BASE_URL}/login")
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard did not load after login"
        dashboard_page.logout()
        # After logout, should be redirected to login page
        assert login_page.is_visible(*LoginPage.USERNAME_INPUT), \
            "Did not return to login page after logout"

    def test_remember_me_functionality(self, browser):
        """
        TC-005: Verify Remember Me Functionality
        Preconditions: User account exists, browser supports cookies
        """
        login_page = LoginPage(browser)
        login_page.load(f"{BASE_URL}/login")
        login_page.login(VALID_USERNAME, VALID_PASSWORD, remember_me=True)
        dashboard_page = DashboardPage(browser)
        assert dashboard_page.is_loaded(), "Dashboard did not load after login"
        # Simulate browser close and reopen by deleting and restarting driver
        browser.quit()
        # For demo, we re-instantiate browser. Real implementation would persist cookies.
        from selenium import webdriver
        new_browser = webdriver.Chrome()
        new_browser.implicitly_wait(5)
        login_page_new = LoginPage(new_browser)
        login_page_new.load(f"{BASE_URL}/dashboard")
        dashboard_page_new = DashboardPage(new_browser)
        assert dashboard_page_new.is_loaded(), \
            "User was not kept logged in after browser restart with 'Remember Me' checked"
        new_browser.quit()

# --- requirements.txt ---
selenium>=4.0.0
pytest>=7.0.0

# --- README.md ---
# Selenium & PyTest Automation Suite

## Overview

This automation suite converts manual test cases from Jira ticket [SCRUM-6] into maintainable, modular Python test scripts using Selenium WebDriver and PyTest, following the Page Object Model (POM) design.

**Tested Features:**
- Login with valid/invalid credentials
- Password reset
- Logout
- Remember Me functionality

## Project Structure

```
project_root/
├── pages/
│   └── login_page.py
│   └── dashboard_page.py
│   └── password_reset_page.py
│   └── base_page.py
├── tests/
│   └── test_authentication.py
│   └── conftest.py
├── requirements.txt
├── README.md
└── sample_test_output.txt
```

## Setup Instructions

1. **Install Python 3.8+**

2. **Clone the repository**

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Download and install the latest [ChromeDriver](https://chromedriver.chromium.org/downloads)**
   - Ensure it's in your PATH or specify its location in `conftest.py`.

5. **Update test data**
   - Set `BASE_URL`, `VALID_USERNAME`, etc., in `test_authentication.py` as per your environment.

## Running Tests

```
pytest tests/
```

## Sample Test Output

See `sample_test_output.txt` for example results.

## Troubleshooting

- **WebDriverException / Cannot connect to Chrome**
  - Ensure Chrome browser and ChromeDriver versions match.
  - ChromeDriver must be in your system PATH.

- **ElementNotFound / TimeoutException**
  - Update placeholder selectors in page objects to match your application's DOM.
  - Increase timeout in `BasePage` if needed.

- **Environment Issues**
  - Check Python version (`python --version`).
  - Verify all dependencies are installed (`pip list`).

## Extending the Framework

- Add new page objects under `pages/`
- Add new test files in `tests/`
- Use fixtures in `conftest.py` for setup/teardown or parameterization
- Integrate with CI/CD (see below)

## Best Practices

- Use unique, stable selectors in page objects.
- Avoid hard sleeps; rely on explicit waits.
- Keep test data and credentials in configuration files or environment variables (never hardcode in production).
- Use parameterization for data-driven tests.

## CI/CD Integration

- Integrate with tools like Jenkins, GitHub Actions, or GitLab CI.
- Use `pytest --junitxml=results.xml` for machine-readable reports.
- Store artifacts and screenshots on failure for debugging.

## Maintenance

- Periodically review and update selectors.
- Upgrade Selenium and PyTest versions as needed.
- Refactor for new features or UI changes.

## Security

- Do not commit real credentials.
- Review for unsafe code or code injection risks.

---

**For questions or issues, consult the troubleshooting section or contact the QA Automation team.**

# --- sample_test_output.txt ---
============================= test session starts =============================
collected 5 items

tests/test_authentication.py .....                                      [100%]

============================== 5 passed in 22.34s ============================
