# test_scrum_6_login.py
"""
Production-ready Selenium automation script generated from Jira SCRUM-6 manual test case JSON.
Test Case: Verify login functionality
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# Logging setup
logging.basicConfig(
    filename='test_scrum_6_login.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture to initialize and teardown Selenium WebDriver.
    Headless Chrome is used for CI/CD compatibility.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    # Optional: set ChromeDriver path via environment variable
    chrome_driver_path = os.getenv('CHROMEDRIVER_PATH', 'chromedriver')
    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=options)
    logging.info("WebDriver initialized.")
    yield driver
    driver.quit()
    logging.info("WebDriver terminated.")

def test_scrum_6_login(driver):
    """
    Test: Verify login functionality
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
        logging.info(f"Navigated to {login_url}")

        # Step 2: Enter valid username and password
        username_selector = "#username"
        password_selector = "#password"
        username = "valid_user"  # Replace with valid test user
        password = "valid_password"  # Replace with valid test password

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
        )
        driver.find_element(By.CSS_SELECTOR, username_selector).clear()
        driver.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))
        )
        driver.find_element(By.CSS_SELECTOR, password_selector).clear()
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
        dashboard_selector = "#dashboard"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, dashboard_selector))
        )
        assert driver.current_url.endswith("/dashboard"), "User not redirected to dashboard"
        logging.info("Assertion passed: User redirected to dashboard.")

        # Optionally, check welcome message
        welcome_selector = "#welcome-message"
        expected_welcome = "Welcome, valid_user!"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, welcome_selector))
        )
        actual_welcome = driver.find_element(By.CSS_SELECTOR, welcome_selector).text
        assert actual_welcome == expected_welcome, f"Unexpected welcome message: {actual_welcome}"
        logging.info("Assertion passed: Welcome message correct.")

        # Attach screenshot for reporting
        screenshot_path = "screenshot1.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")

    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")
