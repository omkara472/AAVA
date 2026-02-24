import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    filename='test_execution.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def wait_for_element(driver, selector, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except Exception as e:
        logging.error(f"Element with selector '{selector}' not found: {e}")
        raise

@pytest.mark.parametrize("test_case", [
    {
      "id": "SCRUM-6",
      "title": "Verify login functionality",
      "description": "Ensure user can log in with valid credentials",
      "steps": [
        "Navigate to login page",
        "Enter valid username and password",
        "Click login button"
      ],
      "expectedResult": "User is redirected to dashboard",
      "tags": ["login", "authentication"],
      "attachments": ["screenshot1.png"]
    },
    {
      "id": "SCRUM-7",
      "title": "Validate password reset",
      "description": "Check password reset functionality",
      "steps": [
        "Click 'Forgot Password'",
        "Enter registered email",
        "Submit request"
      ],
      "expectedResult": "Password reset email is sent",
      "tags": ["password", "reset"],
      "attachments": []
    }
])
def test_jira_case(driver, test_case):
    try:
        logging.info(f"Starting test case: {test_case['id']} - {test_case['title']}")
        if test_case['id'] == "SCRUM-6":
            driver.get("https://example.com/login")
            wait_for_element(driver, "#username").send_keys("testuser")
            wait_for_element(driver, "#password").send_keys("password123")
            wait_for_element(driver, "#login-button").click()
            dashboard_url = "https://example.com/dashboard"
            WebDriverWait(driver, 10).until(EC.url_to_be(dashboard_url))
            assert driver.current_url == dashboard_url, "User not redirected to dashboard"
            logging.info("Login test passed: User redirected to dashboard.")
        elif test_case['id'] == "SCRUM-7":
            driver.get("https://example.com/login")
            wait_for_element(driver, "#forgot-password-link").click()
            wait_for_element(driver, "#email").send_keys("testuser@example.com")
            wait_for_element(driver, "#reset-submit").click()
            confirmation_selector = "#reset-confirmation"
            confirmation_text = wait_for_element(driver, confirmation_selector).text
            assert "Password reset email is sent" in confirmation_text, "Reset confirmation not found"
            logging.info("Password reset test passed: Confirmation message displayed.")
        else:
            pytest.skip(f"Test case {test_case['id']} not automated.")
    except AssertionError as ae:
        logging.error(f"Assertion failed in test case {test_case['id']}: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Error in test case {test_case['id']}: {e}")
        pytest.fail(str(e))
