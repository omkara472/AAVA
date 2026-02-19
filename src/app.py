import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    filename='logs/test_execution.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Setup Chrome WebDriver with headless option."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    try:
        driver = webdriver.Chrome(options=options)
        logging.info("Chrome WebDriver initialized successfully.")
        yield driver
    except Exception as e:
        logging.error(f"WebDriver initialization failed: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Chrome WebDriver closed.")

def test_verify_login_functionality(driver):
    """
    Test Case ID: SCRUM-6
    Title: Verify login functionality
    Description: Ensure user can log in with valid credentials
    Tags: login, authentication
    Attachments: screenshot1.png
    """
    try:
        # Step 1: Navigate to login page
        login_url = "https://example.com/login"
        driver.get(login_url)
        logging.info(f"Navigated to {login_url}")

        # Step 2: Enter valid username and password
        username = "valid_user"
        password = "valid_password"
        # Wait for username field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        logging.info("Entered password.")

        # Step 3: Click login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-button"))
        )
        driver.find_element(By.CSS_SELECTOR, "#login-button").click()
        logging.info("Clicked login button.")

        # Assertion: User is redirected to dashboard
        dashboard_url = "https://example.com/dashboard"
        WebDriverWait(driver, 10).until(
            EC.url_to_be(dashboard_url)
        )
        assert driver.current_url == dashboard_url, \
            f"Expected to be redirected to {dashboard_url}, but got {driver.current_url}"

        # Optionally, check for dashboard element
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#dashboard"))
        )
        logging.info("Dashboard loaded successfully.")

        # Attach screenshot for evidence
        screenshot_path = "logs/screenshot1.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        logging.error(f"Test failed: {e}")
        pytest.fail(f"Test failed due to exception: {e}")
