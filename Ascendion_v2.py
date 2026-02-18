import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import os

# Logging configuration
logging.basicConfig(
    filename='test_suite.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    """Setup Selenium WebDriver with browser options from configuration."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1200,800')
    # Optional: Add more options as needed
    service = Service()  # Default ChromeDriver, assumes chromedriver is in PATH
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver started successfully.")
        yield driver
    except Exception as e:
        logging.error(f"WebDriver failed to start: {e}")
        raise
    finally:
        driver.quit()
        logging.info("WebDriver quit.")

def safe_find(driver, selector, timeout=5):
    """Find element safely with error handling."""
    try:
        return driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        logging.error(f"Element not found: {selector}")
        pytest.fail(f"Element not found: {selector}")
    except Exception as e:
        logging.error(f"Error finding element {selector}: {e}")
        pytest.fail(f"Error finding element {selector}: {e}")

def test_login(driver):
    """Login Test: Validates successful login and welcome message."""
    try:
        driver.get("https://example.com/login")
        logging.info("Navigated to login page.")
        safe_find(driver, "#username").send_keys("testuser")
        safe_find(driver, "#password").send_keys("password123")
        safe_find(driver, "#login-button").click()
        welcome_message = safe_find(driver, "#welcome-message").text
        assert welcome_message == "Welcome, testuser!", \
            f"Expected welcome message, got: {welcome_message}"
        logging.info("Login test passed.")
    except AssertionError as ae:
        logging.error(f"Assertion failed in login test: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Unexpected error in login test: {e}")
        pytest.fail(str(e))

def test_logout(driver):
    """Logout Test: Validates logout and login button presence."""
    try:
        driver.get("https://example.com/dashboard")
        logging.info("Navigated to dashboard.")
        safe_find(driver, "#logout-button").click()
        login_button_text = safe_find(driver, "#login-button").text
        assert login_button_text == "Login", \
            f"Expected 'Login' button after logout, got: {login_button_text}"
        logging.info("Logout test passed.")
    except AssertionError as ae:
        logging.error(f"Assertion failed in logout test: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Unexpected error in logout test: {e}")
        pytest.fail(str(e))
