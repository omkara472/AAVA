import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    filename='test_user_registration.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Setup Chrome WebDriver with headless option and teardown after tests."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_user_registration(driver):
    """
    Test Case: Verify user registration
    Steps:
      1. Navigate to the registration page
      2. Enter valid user details (name, email, password)
      3. Submit the registration form
    Expected Result:
      - User receives a confirmation email and can log in with the new credentials.
    """
    try:
        logging.info("Step 1: Navigating to the registration page")
        driver.get("https://example.com/register")  # Replace with actual registration URL

        # Step 2: Enter valid user details
        logging.info("Step 2: Entering valid user details")
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#name"))
        )
        email_field = driver.find_element(By.CSS_SELECTOR, "#email")
        password_field = driver.find_element(By.CSS_SELECTOR, "#password")

        name_field.clear()
        name_field.send_keys("Test User")
        email_field.clear()
        email_field.send_keys("testuser@example.com")
        password_field.clear()
        password_field.send_keys("Password123!")

        # Step 3: Submit the registration form
        logging.info("Step 3: Submitting the registration form")
        submit_button = driver.find_element(By.CSS_SELECTOR, "#register-button")
        submit_button.click()

        # Validation: Confirmation message
        logging.info("Validating confirmation message")
        confirmation = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#confirmation-message"))
        )
        assert "confirmation email" in confirmation.text.lower(), \
            "Expected confirmation message not found."

        # Optional: Validate login with new credentials
        logging.info("Validating login with new credentials")
        driver.get("https://example.com/login")  # Replace with actual login URL
        login_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login-email"))
        )
        login_password = driver.find_element(By.CSS_SELECTOR, "#login-password")
        login_email.clear()
        login_email.send_keys("testuser@example.com")
        login_password.clear()
        login_password.send_keys("Password123!")
        login_button = driver.find_element(By.CSS_SELECTOR, "#login-button")
        login_button.click()

        welcome_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#welcome-message"))
        )
        assert "welcome" in welcome_message.text.lower(), \
            "User was not able to log in after registration."

        logging.info("Test passed: User registration and login successful.")

    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")
