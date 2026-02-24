"""
Production-ready Selenium script generated from Jira test case SCRUM-6.

Test Scenario: Verify login functionality
Description: Ensure user can log in with valid credentials
Tags: login, authentication
Attachments: screenshot1.png

Requirements:
- Python 3.8+
- selenium
- pytest
- ChromeDriver (in PATH)
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(filename='test_login.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_login_functionality(driver):
    """
    Test Case ID: SCRUM-6
    Title: Verify login functionality
    Steps:
      1. Navigate to login page
      2. Enter valid username and password
      3. Click login button
    Expected Result: User is redirected to dashboard
    """
    try:
        logging.info("Step 1: Navigating to login page")
        driver.get("https://example.com/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )

        logging.info("Step 2: Entering valid username and password")
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("testuser")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("password123")

        logging.info("Step 3: Clicking login button")
        driver.find_element(By.CSS_SELECTOR, "#login-button").click()

        logging.info("Step 4: Waiting for dashboard redirection")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dashboard"))
        )

        logging.info("Step 5: Validating expected result")
        assert driver.current_url.endswith("/dashboard"), \
            "User is not redirected to dashboard"

        logging.info("Test Passed: User successfully redirected to dashboard")

        # Optionally, save screenshot for reporting
        driver.save_screenshot("screenshot1.png")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Test Failed: Element not found or timeout - {str(e)}")
        pytest.fail(f"Test Failed: Element not found or timeout - {str(e)}")
    except AssertionError as ae:
        logging.error(f"Test Failed: Assertion error - {str(ae)}")
        pytest.fail(f"Test Failed: Assertion error - {str(ae)}")
    except Exception as ex:
        logging.error(f"Test Failed: Unexpected error - {str(ex)}")
        pytest.fail(f"Test Failed: Unexpected error - {str(ex)}")
