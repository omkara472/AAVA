# test_registration_workflow.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# Configure logging
logging.basicConfig(
    filename='test_registration_workflow.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture to initialize and teardown Selenium WebDriver.
    Uses Chrome in headless mode for CI/CD compatibility.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    service = Service()
    driver = webdriver.Chrome(options=options, service=service)
    yield driver
    driver.quit()

def wait_for_element(driver, selector, timeout=10):
    """
    Wait for element to be present in DOM and visible.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except Exception as e:
        logging.error(f"Timeout waiting for element '{selector}': {e}")
        raise

def test_registration_workflow(driver):
    """
    Test Case: Verify user registration workflow
    Steps:
      1. Navigate to the registration page
      2. Enter valid user details (name, email, password)
      3. Submit the registration form
    Expected Result:
      User receives confirmation email and is able to log in
    """
    try:
        # Step 1: Navigate to the registration page
        registration_url = "https://example.com/register"  # Replace with actual URL
        driver.get(registration_url)
        logging.info("Navigated to registration page.")

        # Step 2: Enter valid user details
        # NOTE: Update selectors as per actual application
        name_selector = "#name"
        email_selector = "#email"
        password_selector = "#password"
        submit_selector = "#register-button"

        name = "Test User"
        email = "testuser@example.com"
        password = "SecurePass123!"

        wait_for_element(driver, name_selector).send_keys(name)
        wait_for_element(driver, email_selector).send_keys(email)
        wait_for_element(driver, password_selector).send_keys(password)
        logging.info("Entered user details.")

        # Step 3: Submit the registration form
        wait_for_element(driver, submit_selector).click()
        logging.info("Submitted registration form.")

        # Step 4: Assert confirmation message
        confirmation_selector = "#confirmation-message"
        confirmation_text_expected = "Registration successful! Please check your email."

        confirmation_element = wait_for_element(driver, confirmation_selector)
        confirmation_text_actual = confirmation_element.text.strip()
        assert confirmation_text_actual == confirmation_text_expected, \
            f"Expected confirmation '{confirmation_text_expected}', got '{confirmation_text_actual}'"
        logging.info("Confirmed registration success.")

        # Step 5: (Optional) Attempt login to verify user creation
        # This step can be implemented if login page and flow are available.

    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
