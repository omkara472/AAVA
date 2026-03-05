# test_cases_selenium.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time

# Configure logging
logging.basicConfig(filename='test_execution.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    try:
        driver.save_screenshot(name)
        logging.info(f"Screenshot saved: {name}")
    except Exception as e:
        logging.error(f"Failed to save screenshot: {e}")

def test_verify_user_registration(driver):
    """
    Test Case: SCRUM-6
    Title: Verify user registration
    Description: Ensure new users can register with valid information.
    Tags: registration, user, manual
    Attachments: reg_screenshot1.png
    """
    try:
        # Step 1: Navigate to registration page
        driver.get("https://example.com/register")
        logging.info("Navigated to registration page.")

        # Step 2: Enter valid user details
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("newuser")
        driver.find_element(By.CSS_SELECTOR, "#email").send_keys("newuser@example.com")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("securePassword123")
        logging.info("Entered valid user details.")

        # Step 3: Submit registration form
        driver.find_element(By.CSS_SELECTOR, "#register-button").click()
        logging.info("Submitted registration form.")

        # Wait for confirmation message
        time.sleep(2)
        confirmation = driver.find_element(By.CSS_SELECTOR, "#confirmation-message").text
        expected = "User account is created and confirmation email is sent."
        assert expected in confirmation, f"Expected '{expected}', got '{confirmation}'"
        logging.info("Registration confirmed.")

        # Attach screenshot
        take_screenshot(driver, "reg_screenshot1.png")

    except Exception as e:
        logging.error(f"Test SCRUM-6 failed: {e}")
        take_screenshot(driver, "SCRUM-6_failure.png")
        raise

def test_validate_login_functionality(driver):
    """
    Test Case: SCRUM-7
    Title: Validate login functionality
    Description: Check that users can log in with correct credentials.
    Tags: login, authentication, manual
    Attachments: None
    """
    try:
        # Step 1: Go to login page
        driver.get("https://example.com/login")
        logging.info("Navigated to login page.")

        # Step 2: Enter valid username and password
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("newuser")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("securePassword123")
        logging.info("Entered login credentials.")

        # Step 3: Click login button
        driver.find_element(By.CSS_SELECTOR, "#login-button").click()
        logging.info("Clicked login button.")

        # Wait for dashboard redirection
        time.sleep(2)
        assert driver.current_url == "https://example.com/dashboard", \
            f"Expected dashboard URL, got {driver.current_url}"
        logging.info("User redirected to dashboard.")

    except Exception as e:
        logging.error(f"Test SCRUM-7 failed: {e}")
        take_screenshot(driver, "SCRUM-7_failure.png")
        raise

# test_cases_pytest.py
import pytest

@pytest.mark.parametrize("test_case", [
    {
        "id": "SCRUM-6",
        "title": "Verify user registration",
        "steps": [
            {"action": "open_url", "value": "https://example.com/register"},
            {"action": "input", "selector": "#username", "value": "newuser"},
            {"action": "input", "selector": "#email", "value": "newuser@example.com"},
            {"action": "input", "selector": "#password", "value": "securePassword123"},
            {"action": "click", "selector": "#register-button"},
            {"action": "assert", "selector": "#confirmation-message",
             "expected": "User account is created and confirmation email is sent."}
        ]
    },
    {
        "id": "SCRUM-7",
        "title": "Validate login functionality",
        "steps": [
            {"action": "open_url", "value": "https://example.com/login"},
            {"action": "input", "selector": "#username", "value": "newuser"},
            {"action": "input", "selector": "#password", "value": "securePassword123"},
            {"action": "click", "selector": "#login-button"},
            {"action": "assert_url", "expected": "https://example.com/dashboard"}
        ]
    }
])
def test_case_runner(driver, test_case):
    for step in test_case["steps"]:
        action = step["action"]
        if action == "open_url":
            driver.get(step["value"])
        elif action == "input":
            driver.find_element(By.CSS_SELECTOR, step["selector"]).send_keys(step["value"])
        elif action == "click":
            driver.find_element(By.CSS_SELECTOR, step["selector"]).click()
        elif action == "assert":
            assert step["expected"] in driver.find_element(By.CSS_SELECTOR, step["selector"]).text
        elif action == "assert_url":
            assert driver.current_url == step["expected"]
