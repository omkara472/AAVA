import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    filename='test_registration_flow.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Setup and teardown for Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_user_registration_flow(driver):
    """
    Test Case: Verify user registration flow
    Steps:
      1. Navigate to the registration page
      2. Enter valid user details (name, email, password)
      3. Submit the registration form
      4. Check email inbox for confirmation email
      5. Click the confirmation link
    Expected Result:
      User account is created and activated; confirmation email is received and link works.
    """
    try:
        # Step 1: Navigate to the registration page
        registration_url = "https://example.com/register"
        driver.get(registration_url)
        logging.info("Navigated to registration page: %s", registration_url)

        # Step 2: Enter valid user details
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#name"))
        )
        driver.find_element(By.CSS_SELECTOR, "#name").send_keys("Test User")
        driver.find_element(By.CSS_SELECTOR, "#email").send_keys("testuser@example.com")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("Password123!")
        logging.info("Entered user details.")

        # Step 3: Submit the registration form
        driver.find_element(By.CSS_SELECTOR, "#register-button").click()
        logging.info("Submitted registration form.")

        # Step 4: Check for confirmation message (simulate email inbox check)
        # In real automation, email verification would be handled via API or email client integration.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#confirmation-message"))
        )
        confirmation_text = driver.find_element(By.CSS_SELECTOR, "#confirmation-message").text
        assert "confirmation email" in confirmation_text.lower(), "Confirmation message not found."
        logging.info("Confirmation message received: %s", confirmation_text)

        # Step 5: Simulate clicking confirmation link (assume link in confirmation message)
        # For demonstration, click a link if present
        try:
            confirmation_link = driver.find_element(By.CSS_SELECTOR, "#confirmation-link")
            confirmation_link.click()
            logging.info("Clicked confirmation link.")
        except Exception as e:
            logging.warning("Confirmation link not found: %s", e)

        # Final assertion: User account is activated (simulate by checking profile page)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#profile-page"))
        )
        profile_header = driver.find_element(By.CSS_SELECTOR, "#profile-page").text
        assert "Test User" in profile_header, "User profile not activated."
        logging.info("User account activated and profile page loaded.")

    except AssertionError as ae:
        logging.error("Assertion failed: %s", ae)
        pytest.fail(str(ae))
    except Exception as ex:
        logging.error("Unexpected error: %s", ex)
        pytest.fail("Test failed due to unexpected error: %s" % ex)
