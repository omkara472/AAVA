# Selenium PyTest Automation Suite

## Overview

This project automates authentication test cases extracted from Jira ticket `SCRUM-6`, originally authored as manual tests in Excel. The suite uses the Page Object Model (POM) with Selenium WebDriver and PyTest, ensuring maintainability, extensibility, and robust error handling.

## Project Structure

```
project/
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   └── test_auth_workflow.py
├── conftest.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**

    ```bash
    git clone <repo-url>
    cd project
    ```

2. **Create a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have Chrome and ChromeDriver installed.**
    - Download ChromeDriver: https://sites.google.com/chromium.org/driver/

5. **Configure the base URL**
    - Update `base_url` fixture in `conftest.py` as needed.

## Running Tests

```bash
pytest tests/
```

To run tests in parallel:

```bash
pytest -n auto tests/
```

## Test Cases

- **TC-001**: Verify Login Functionality
- **TC-002**: Validate Forgot Password Workflow
- **TC-003**: Check Login with Invalid Credentials
- **TC-004**: Verify Session Timeout (skipped by default; see code comments)

## Sample Output

```
$ pytest tests/
=========================== test session starts ============================
collected 4 items

tests/test_auth_workflow.py::TestAuthWorkflow::test_verify_login_functionality PASSED
tests/test_auth_workflow.py::TestAuthWorkflow::test_validate_forgot_password_workflow PASSED
tests/test_auth_workflow.py::TestAuthWorkflow::test_check_login_with_invalid_credentials PASSED
tests/test_auth_workflow.py::TestAuthWorkflow::test_verify_session_timeout SKIPPED

==================== 3 passed, 1 skipped in 7.00s ===========================
```

## Troubleshooting

- **WebDriverException**: Ensure ChromeDriver matches your Chrome version and is in your PATH.
- **TimeoutException**: Increase the `timeout` in `BasePage` or check selector accuracy.
- **ElementNotInteractableException**: Wait for element to be visible/clickable, or update selectors.

## Extensibility & Best Practices

- **Add more page objects** to `pages/` as your app grows.
- **Parameterize test data** using PyTest fixtures or external files.
- **Integrate with CI/CD**: Add to your pipeline using `pytest` command.
- **Reporting**: Use `pytest-html` or `allure-pytest` for advanced reporting.

## Recommendations for Future Enhancements

- Support additional test management integrations (e.g., Jira XRay, Zephyr).
- Add support for other browsers (Firefox, Edge) via configuration.
- Implement batch test case generation and data-driven testing.
- Enhance selectors with more robust strategies (data-test-id, XPath).

## Security

- No unsafe operations or code injection is performed.
- Credentials and sensitive data should be managed securely (e.g., with environment variables or secrets management).

## Maintenance

- Regularly update `requirements.txt` for latest Selenium/PyTest.
- Review and update selectors as application UI changes.
- Refactor page objects to reduce duplication.
