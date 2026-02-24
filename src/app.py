# src/test_scrum_login.py

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
    filename='test_scrum_login.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and quit Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    # Optional: Set path to ChromeDriver if not in PATH
    # service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_scrum_6_login_functionality(driver):
    """
    Test Case: SCRUM-6
    Title: Verify login functionality
    Description: Ensure user can log in with valid credentials
    Steps:
      1. Navigate to login page
      2. Enter valid username and password
      3. Click login button
    Expected Result: User is redirected to dashboard
    Tags: login, authentication
    Attachments: screenshot1.png
    """
    try:
        # Step 1: Navigate to login page
        login_url = "https://example.com/login"  # Update with actual URL if known
        driver.get(login_url)
        logging.info("Navigated to login page: %s", login_url)

        # Step 2: Enter valid username and password
        username_selector = "#username"
        password_selector = "#password"
        username = "valid_user"  # Replace with actual test data
        password = "valid_password"  # Replace with actual test data

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
        )
        driver.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))
        )
        driver.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
        logging.info("Entered password.")

        # Step 3: Click login button
        login_button_selector = "#login-button"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector))
        )
        driver.find_element(By.CSS_SELECTOR, login_button_selector).click()
        logging.info("Clicked login button.")

        # Assertion: User is redirected to dashboard
        dashboard_selector = "#dashboard"  # Update with actual dashboard selector
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, dashboard_selector))
        )
        dashboard_text = driver.find_element(By.CSS_SELECTOR, dashboard_selector).text
        assert "Welcome" in dashboard_text or "Dashboard" in dashboard_text, \
            f"Expected dashboard welcome, got: {dashboard_text}"
        logging.info("Assertion passed: User is redirected to dashboard.")

        # Save screenshot for evidence/attachment
        screenshot_path = os.path.join(os.getcwd(), "screenshot1.png")
        driver.save_screenshot(screenshot_path)
        logging.info("Screenshot saved: %s", screenshot_path)

    except Exception as e:
        logging.error("Test failed: %s", str(e))
        pytest.fail(f"SCRUM-6 Login Test failed: {str(e)}")
