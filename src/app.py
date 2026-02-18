# test_scrum_6_login.py

"""
Production-ready Selenium automation script generated from Jira SCRUM-6 test case.
- Scenario: Login functionality test
- Source: https://omkarmareedu472.atlassian.net/browse/SCRUM-6
- Attachments: login_screen.png (refer to documentation for usage)
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    filename='test_scrum_6.log',
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
    service = Service()  # Default ChromeDriver path, ensure chromedriver is in PATH
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver started successfully.")
        yield driver
    except Exception as e:
        logging.error(f"WebDriver initialization failed: {e}")
        raise
    finally:
        driver.quit()
        logging.info("WebDriver closed.")

def test_scrum_6_login(driver):
    """
    Test Case: SCRUM-6 - Login Test
    Steps:
      1. Open the application
      2. Navigate to the login page
      3. Enter valid credentials
      4. Click the login button
    Expected Result: User is successfully logged in and redirected to the dashboard.
    Tags: login, smoke, regression
    """
    try:
        # Step 1: Open the application (Assume base URL is provided)
        base_url = "https://example.com"  # Replace with actual application URL
        driver.get(base_url)
        logging.info(f"Opened application URL: {base_url}")

        # Step 2: Navigate to the login page
        login_url = f"{base_url}/login"
        driver.get(login_url)
        logging.info(f"Navigated to login page: {login_url}")

        # Step 3: Enter valid credentials
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("testuser")
        logging.info("Entered username.")

        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("password123")
        logging.info("Entered password.")

        # Step 4: Click the login button
        driver.find_element(By.CSS_SELECTOR, "#login-button").click()
        logging.info("Clicked login button.")

        # Assertion: User is successfully logged in and redirected to the dashboard
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#welcome-message"))
        )
        welcome_text = driver.find_element(By.CSS_SELECTOR, "#welcome-message").text
        assert welcome_text == "Welcome, testuser!", \
            f"Expected welcome message not found. Actual: '{welcome_text}'"
        logging.info("Login assertion passed.")

    except Exception as e:
        logging.error(f"Test SCRUM-6 failed: {e}")
        pytest.fail(f"Test SCRUM-6 failed: {e}")

# Documentation, configuration, troubleshooting, and test report are included in the operation log and README.
