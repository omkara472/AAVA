"""
Production-ready Selenium automation script generated from Jira manual test case SCRUM-6.

Test Case: Verify login functionality
Description: Ensure user can log in with valid credentials
Steps:
    1. Navigate to login page
    2. Enter valid username and password
    3. Click login button
Expected Result: User is redirected to dashboard

Tags: login, authentication
Attachments: screenshot1.png
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# Configure logging
logging.basicConfig(
    filename='test_login_functionality.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture for Selenium WebDriver setup and teardown.
    Uses Chrome in headless mode for CI/CD compatibility.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    logging.info("WebDriver initialized.")
    yield driver
    driver.quit()
    logging.info("WebDriver terminated.")

def test_login_functionality(driver):
    """
    Test: Verify login functionality (SCRUM-6)
    Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
    Expected Result: User is redirected to dashboard
    """
    try:
        # Step 1: Navigate to login page
        login_url = "https://example.com/login"
        driver.get(login_url)
        logging.info(f"Navigated to login page: {login_url}")

        # Step 2: Enter valid username and password
        username = "testuser"
        password = "password123"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
        logging.info(f"Entered username: {username}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dashboard"))
        )
        dashboard_url = driver.current_url
        assert "/dashboard" in dashboard_url, "User was not redirected to dashboard."
        logging.info(f"User redirected to dashboard: {dashboard_url}")

        # Optionally, check for welcome message
        try:
            welcome_message = driver.find_element(By.CSS_SELECTOR, "#welcome-message").text
            assert welcome_message == "Welcome, testuser!", "Welcome message incorrect."
            logging.info("Welcome message validated.")
        except NoSuchElementException:
            logging.warning("Welcome message not found; skipping assertion.")

        # Optionally, save screenshot for reporting
        screenshot_path = os.path.join(os.getcwd(), "screenshot1.png")
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Test failed due to element error: {str(e)}")
        pytest.fail(f"Test failed due to element error: {str(e)}")
    except AssertionError as ae:
        logging.error(f"Assertion failed: {str(ae)}")
        pytest.fail(f"Assertion failed: {str(ae)}")
    except Exception as ex:
        logging.error(f"Unexpected error: {str(ex)}")
        pytest.fail(f"Unexpected error: {str(ex)}")
