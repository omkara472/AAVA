#src/test_login_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(
    filename='test_execution.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    logging.info("WebDriver started.")
    yield driver
    driver.quit()
    logging.info("WebDriver quit.")

def wait_for_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        logging.info(f"Element found: {selector}")
        return element
    except TimeoutException:
        logging.error(f"Timeout waiting for element: {selector}")
        raise

def test_login(driver):
    try:
        driver.get("https://example.com/login")
        logging.info("Navigated to login page.")
        username_field = wait_for_element(driver, "#username")
        username_field.clear()
        username_field.send_keys("valid_user")
        logging.info("Entered username.")
        password_field = wait_for_element(driver, "#password")
        password_field.clear()
        password_field.send_keys("valid_password")
        logging.info("Entered password.")
        login_button = wait_for_element(driver, "#login-button")
        login_button.click()
        logging.info("Clicked login button.")
        dashboard_url = "https://example.com/dashboard"
        WebDriverWait(driver, 10).until(EC.url_to_be(dashboard_url))
        assert driver.current_url == dashboard_url, "User not redirected to dashboard"
        logging.info("User redirected to dashboard.")
        welcome_selector = "#welcome-message"
        welcome_message = wait_for_element(driver, welcome_selector)
        assert "Welcome" in welcome_message.text, "Welcome message not found"
        logging.info("Welcome message validated.")
    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        pytest.fail(str(e))

tests/test_login_pytest.py

import pytest

@pytest.mark.usefixtures("driver")
def test_login(driver):
    from src.test_login_selenium import test_login as selenium_test_login
    selenium_test_login(driver)
