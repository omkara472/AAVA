"""
Production-ready Selenium script generated from Jira JSON test specification.
Test Case: SCRUM-6 - Verify login functionality
Description: Ensure user can log in with valid credentials
Tags: login, authentication
Attachments: screenshot1.png
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# Configure logging
logging.basicConfig(
    filename='test_jira_login.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and teardown Selenium WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    # You can add more options as needed

    # Path to chromedriver can be set via environment variable or default location
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH', 'chromedriver')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logging.info("WebDriver initialized.")
    yield driver
    driver.quit()
    logging.info("WebDriver terminated.")

def test_verify_login_functionality(driver):
    """
    Test SCRUM-6: Verify login functionality
    Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
    Expected Result:
        User is redirected to dashboard
    """
    try:
        # Step 1: Navigate to login page
        login_url = "https://example.com/login"
        driver.get(login_url)
        logging.info(f"Navigated to login page: {login_url}")

        # Step 2: Enter valid username and password
        username_selector = "#username"
        password_selector = "#password"
        username = "valid_user"  # Replace with actual test data
        password = "valid_password"  # Replace with actual test data

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
        )
        driver.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
        logging.info(f"Entered username: {username}")

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
        dashboard_url = "https://example.com/dashboard"  # Replace with actual dashboard URL if needed
        WebDriverWait(driver, 10).until(
            EC.url_contains("dashboard")
        )
        assert "dashboard" in driver.current_url, "User was not redirected to dashboard."
        logging.info("User successfully redirected to dashboard.")

        # Optionally, verify dashboard element presence
        dashboard_selector = "#dashboard-main"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, dashboard_selector))
        )
        logging.info("Dashboard main element found.")

        # Save screenshot for evidence
        screenshot_path = "screenshot1.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Test failed due to element not found or timeout: {e}")
        pytest.fail(f"Test failed: {e}")
    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
        pytest.fail(f"Assertion failed: {ae}")
    except Exception as ex:
        logging.error(f"Unexpected error: {ex}")
        pytest.fail(f"Unexpected error: {ex}")
