"""
Production-ready Selenium script generated from Jira JSON test case SCRUM-6.
Automates login functionality verification with robust error handling and reporting.
"""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Configure logging
logging.basicConfig(
    filename='test_login_selenium.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

LOGIN_URL = "https://example.com/login"
USERNAME = "valid_username"
PASSWORD = "valid_password"
DASHBOARD_URL = "https://example.com/dashboard"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    try:
        driver = webdriver.Chrome(options=options)
        logging.info("Chrome WebDriver started successfully.")
        yield driver
    except Exception as e:
        logging.error(f"WebDriver initialization failed: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Chrome WebDriver closed.")

def login(driver, username, password):
    try:
        driver.get(LOGIN_URL)
        logging.info(f"Navigated to login page: {LOGIN_URL}")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
        logging.info("Entered username.")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        logging.info("Entered password.")
        driver.find_element(By.CSS_SELECTOR, "#login-button").click()
        logging.info("Clicked login button.")
    except Exception as e:
        logging.error(f"Login step failed: {e}")
        raise

def verify_dashboard_redirect(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains(DASHBOARD_URL)
        )
        logging.info("User redirected to dashboard successfully.")
        return True
    except Exception as e:
        logging.error(f"Dashboard redirect verification failed: {e}")
        return False

def test_login_functionality(driver):
    try:
        login(driver, USERNAME, PASSWORD)
        assert verify_dashboard_redirect(driver), "User was not redirected to dashboard."
        logging.info("Test passed: User redirected to dashboard.")
    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Unexpected error during test execution: {e}")
        pytest.fail(str(e))
