# 1. Directory Structure

automation_suite/
│
├── pages/
│   ├── __init__.py
│   ├── login_page.py
│   └── dashboard_page.py
│
├── tests/
│   ├── __init__.py
│   └── test_login.py
│
├── conftest.py
├── requirements.txt
├── README.md
└── sample_test_output.txt

---

# 2. Python Files

## 2.1. pages/login_page.py

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """Page Object for the Login Page."""

    URL = "https://your-app-url.com/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.ID, "login-error")

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        """Navigates to the login page."""
        self.driver.get(self.URL)

    def login(self, username, password):
        """Performs login action with provided credentials."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Returns the login error message, if present."""
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            ).text
        except Exception:
            return None
```

---

## 2.2. pages/dashboard_page.py

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """Page Object for the Dashboard (post-login) Page."""

    WELCOME_BANNER = (By.ID, "welcome-banner")

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        """Checks if dashboard is loaded by verifying the welcome banner."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.WELCOME_BANNER)
            )
            return True
        except Exception:
            return False

    def get_welcome_text(self):
        """Returns the welcome banner text."""
        return self.driver.find_element(*self.WELCOME_BANNER).text
```

---

## 2.3. tests/test_login.py

```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Sample data extracted from standardized JSON
valid_credentials = [
    {"username": "testuser", "password": "correctpass", "expected": "success"},
]

invalid_credentials = [
    {"username": "testuser", "password": "wrongpass", "expected": "Invalid username or password."},
    {"username": "", "password": "somepass", "expected": "Username is required."},
    {"username": "testuser", "password": "", "expected": "Password is required."},
]

@pytest.mark.usefixtures("driver")
class TestLogin:
    """Test cases for Login functionality."""

    @pytest.mark.parametrize("creds", valid_credentials)
    def test_login_success(self, driver, creds):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.load()
        login_page.login(creds["username"], creds["password"])
        assert dashboard_page.is_loaded(), "Dashboard did not load after login."
        assert "Welcome" in dashboard_page.get_welcome_text()

    @pytest.mark.parametrize("creds", invalid_credentials)
    def test_login_invalid(self, driver, creds):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(creds["username"], creds["password"])
        error_msg = login_page.get_error_message()
        assert error_msg == creds["expected"], f"Expected error: {creds['expected']}, got: {error_msg}"
```

---

## 2.4. conftest.py

```python
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests against"
    )

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="function")
def driver(browser):
    """Initializes and yields a Selenium WebDriver instance."""
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

---

# 3. requirements.txt

```
selenium>=4.10.0
pytest>=7.0.0
pytest-html>=3.2.0
```

---

# 4. README.md

```markdown
# Selenium Pytest Automation Suite

## Overview

This suite automates login functionality for your web application using Selenium WebDriver and PyTest, following the Page Object Model (POM) design pattern. The framework is modular, maintainable, and ready for extension to cover more features and test cases.

## Directory Structure

```
automation_suite/
├── pages/
├── tests/
├── conftest.py
├── requirements.txt
├── README.md
└── sample_test_output.txt
```

## Setup Instructions

### 1. Install Python (>=3.7)

Make sure Python is installed. Download from [python.org](https://www.python.org/downloads/).

### 2. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download WebDriver Binaries

- **Chrome:** [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- **Firefox:** [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)

Ensure the driver binary is on your system PATH.

### 4. Run the Tests

```bash
pytest --browser=chrome --html=report.html
```

- Supported browsers: `chrome`, `firefox`
- Default: `chrome`
- The `--html=report.html` option generates an HTML report.

## Usage Examples

- Run all tests: `pytest`
- Run a specific test: `pytest tests/test_login.py`
- Run with a different browser: `pytest --browser=firefox`

## Troubleshooting

### Common Issues

- **WebDriverException:** Ensure the correct driver binary is installed and on PATH.
- **Timeouts:** Increase waits or check for selector changes.
- **ElementNotInteractable:** Page may not be fully loaded; check for explicit waits.

### Environment Configuration

- Confirm Python, pip, and WebDriver versions are compatible.
- If running headless, some UI elements may behave differently.

## Extending the Framework

- Add new Page Objects under `pages/`.
- Add new test cases under `tests/`.
- Use parameterized data in tests for data-driven coverage.
- Add/modify fixtures in `conftest.py` for advanced setup/teardown.

## Best Practices

- Keep selectors up-to-date as the UI evolves.
- Prefer explicit waits over `time.sleep()`.
- Use parameterization for data-driven scenarios.
- Review test reports regularly and address flaky tests.

## CI/CD Integration

- Integrate with tools like Jenkins, GitHub Actions, or GitLab CI.
- Use `pytest --maxfail=1 --disable-warnings --html=report.html` for stable pipelines.
- Archive HTML reports as build artifacts.

## Maintenance

- Update dependencies regularly (`pip list --outdated`).
- Refactor page objects as the application changes.
- Review test coverage and add tests for new features.

## Sample Test Output

See `sample_test_output.txt` for an example of test execution results.

---
```

---

# 5. sample_test_output.txt

```
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/user/automation_suite
plugins: html-3.2.0
collected 4 items

tests/test_login.py::TestLogin::test_login_success[{'username': 'testuser', 'password': 'correctpass', 'expected': 'success'}] PASSED
tests/test_login.py::TestLogin::test_login_invalid[{'username': 'testuser', 'password': 'wrongpass', 'expected': 'Invalid username or password.'}] PASSED
tests/test_login.py::TestLogin::test_login_invalid[{'username': '', 'password': 'somepass', 'expected': 'Username is required.'}] PASSED
tests/test_login.py::TestLogin::test_login_invalid[{'username': 'testuser', 'password': '', 'expected': 'Password is required.'}] PASSED

============================== 4 passed in 11.22s ==============================
```

---

# 6. Notes & Recommendations

- **Security:** No user input is executed directly; all test data is parameterized.
- **Extensibility:** Easily add more page objects and tests.
- **Scalability:** Supports parallel execution via `pytest-xdist` (install and run with `-n auto`).
- **Reporting:** pytest-html is enabled for HTML reports.

---

**This suite is immediately ready for use and extension. Update placeholder URLs and selectors as per your application. For further enhancements, add new page objects and parameterized tests in the existing modular structure.**

If you have additional test cases or new features to automate, simply extend the `pages/` and `tests/` modules using the provided patterns.

---

**End of deliverable.**