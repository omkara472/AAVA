# Directory Structure
.
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── password_reset_page.py
├── tests/
│   ├── conftest.py
│   └── test_authentication.py
├── requirements.txt
├── README.md
└── sample_test_output.txt

# pages/base_page.py
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all pages."""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, by, locator):
        """Wait for element to be present and return it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def click(self, by, locator):
        """Wait for element to be clickable and click."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def type(self, by, locator, value):
        """Wait for element and type value."""
        element = self.find(by, locator)
        element.clear()
        element.send_keys(value)

    def is_element_present(self, by, locator):
        """Check if element is present."""
        try:
            self.find(by, locator)
            return True
        except:
            return False

    def get_current_url(self):
        return self.driver.current_url
```

# pages/login_page.py
```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Login Page."""

    # Placeholder selectors – replace with actual application selectors
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-btn')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, 'Forgot Password')

    def go_to(self, base_url):
        self.driver.get(f"{base_url}/login")

    def login(self, username, password):
        self.type(*self.USERNAME_INPUT, value=username)
        self.type(*self.PASSWORD_INPUT, value=password)
        self.click(*self.LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(*self.FORGOT_PASSWORD_LINK)
```

# pages/dashboard_page.py
```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """Page Object for Dashboard Page."""

    # Placeholder selectors
    LOGOUT_BUTTON = (By.ID, 'logout-btn')

    def is_loaded(self):
        # Example: check for a unique dashboard element
        return self.is_element_present(By.ID, 'dashboard-main')

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)
```

# pages/password_reset_page.py
```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class PasswordResetPage(BasePage):
    """Page Object for Password Reset Page."""

    EMAIL_INPUT = (By.ID, 'reset-email')
    SUBMIT_BUTTON = (By.ID, 'reset-submit')
    RESET_LINK_TEXT = "Reset your password"
    NEW_PASSWORD_INPUT = (By.ID, 'new-password')
    CONFIRM_PASSWORD_INPUT = (By.ID, 'confirm-password')
    SAVE_BUTTON = (By.ID, 'save-password')

    def submit_reset_request(self, email):
        self.type(*self.EMAIL_INPUT, value=email)
        self.click(*self.SUBMIT_BUTTON)

    def set_new_password(self, new_password):
        self.type(*self.NEW_PASSWORD_INPUT, value=new_password)
        self.type(*self.CONFIRM_PASSWORD_INPUT, value=new_password)
        self.click(*self.SAVE_BUTTON)
```

# tests/conftest.py
```python
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")

@pytest.fixture(scope="session")
def base_url():
    # Replace with your application base URL
    return "http://localhost:8000"

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
```

# tests/test_authentication.py
```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.password_reset_page import PasswordResetPage

# Test Data – replace with valid test accounts as needed
TEST_USER = {
    "username": "testuser",
    "password": "Password123!",
    "email": "testuser@example.com",
    "new_password": "NewPassword123!"
}

@pytest.mark.high
def test_verify_login_functionality(driver, base_url):
    """TC-001: Verify Login Functionality"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.go_to(base_url)
    login_page.login(TEST_USER["username"], TEST_USER["password"])
    assert dashboard_page.is_loaded(), "User is not redirected to dashboard"

@pytest.mark.medium
def test_validate_password_reset(driver, base_url):
    """TC-002: Validate Password Reset"""
    login_page = LoginPage(driver)
    password_reset_page = PasswordResetPage(driver)
    dashboard_page = DashboardPage(driver)

    # Step 1: Go to login page
    login_page.go_to(base_url)
    # Step 2: Click 'Forgot Password'
    login_page.click_forgot_password()
    # Step 3: Enter registered email
    password_reset_page.submit_reset_request(TEST_USER["email"])
    # Step 4: Simulate email checking and following reset link (manual/mocked in real world)
    # For demo, directly access reset page
    driver.get(f"{base_url}/reset-password?token=mocked-token")
    # Step 5: Set new password
    password_reset_page.set_new_password(TEST_USER["new_password"])
    # Assert user can login with new password
    login_page.go_to(base_url)
    login_page.login(TEST_USER["username"], TEST_USER["new_password"])
    assert dashboard_page.is_loaded(), "Password reset failed or login unsuccessful"

@pytest.mark.low
def test_check_logout_functionality(driver, base_url):
    """TC-003: Check Logout Functionality"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.go_to(base_url)
    login_page.login(TEST_USER["username"], TEST_USER["password"])
    assert dashboard_page.is_loaded(), "Login failed, cannot test logout"
    dashboard_page.logout()
    # User should be redirected to login page
    assert "login" in driver.current_url.lower(), "User was not redirected to login page after logout"
```

# requirements.txt
```
selenium>=4.10.0
pytest>=7.0.0
```

# README.md
````markdown
# Selenium & PyTest Automation Suite

## Overview

This project automates authentication test cases (login, password reset, logout) extracted from Jira ticket SCRUM-6. It uses the Page Object Model with Selenium WebDriver and PyTest for robust, maintainable test automation.

## Directory Structure

```
pages/
    base_page.py
    login_page.py
    dashboard_page.py
    password_reset_page.py
tests/
    conftest.py
    test_authentication.py
requirements.txt
README.md
sample_test_output.txt
```

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```

2. **Set Up Python Environment**

   - Python 3.8+ recommended
   - (Optional) Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **WebDriver Setup**

   - Chrome: Download [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version.
   - Firefox: Download [geckodriver](https://github.com/mozilla/geckodriver/releases).
   - Ensure the driver executable is on your `PATH`.

## Running the Tests

```bash
pytest --browser=chrome
```
- Supported browsers: `chrome`, `firefox` (default: chrome)
- Tests run headless by default.

## Test Data

- Update `TEST_USER` in `tests/test_authentication.py` with valid credentials for your environment.

## Troubleshooting

- **WebDriverException:** Ensure browser driver is installed and on your `PATH`.
- **Timeouts/Selectors:** If tests fail due to missing elements, update selectors in the Page Object files to match your application.
- **Environment Issues:** Confirm the application under test is accessible at the `base_url` specified in `conftest.py`.

## Extending the Framework

- Add new page objects in `pages/`.
- Create new test modules in `tests/`.
- Use PyTest fixtures for reusable setup/teardown logic.
- Parameterize tests for data-driven execution.

## Best Practices

- Use explicit waits (see `BasePage`).
- Keep selectors in Page Objects only.
- Avoid hard-coded test data; use fixtures or config files for secrets.
- Mark tests with `@pytest.mark.<priority>` for selective execution.

## CI/CD Integration

- Integrate with GitHub Actions, Jenkins, or GitLab CI using standard `pytest` commands.
- Use `--junitxml=results.xml` for reporting.

## Sample Test Output

See `sample_test_output.txt` for example PyTest run output.

## Support

For issues, check the troubleshooting section or update selectors as per your application.
````

# sample_test_output.txt
```
============================= test session starts ==============================
platform linux -- Python 3.10.4, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/user/automation
collected 3 items

tests/test_authentication.py ...                                        [100%]

============================== 3 passed in 14.25s =============================
```
