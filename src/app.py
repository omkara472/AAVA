import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

logging.basicConfig(
    filename='test_registration.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    logging.info("Chrome WebDriver started in headless mode.")
    yield driver
    driver.quit()
    logging.info("Chrome WebDriver quit.")

def take_screenshot(driver, name):
    screenshot_path = os.path.join(os.getcwd(), name)
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot saved: {screenshot_path}")

def test_registration(driver):
    try:
        registration_url = "https://example.com/register"
        driver.get(registration_url)
        logging.info(f"Navigated to registration page: {registration_url}")
        take_screenshot(driver, "registration_page.png")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("newuser123")
        driver.find_element(By.CSS_SELECTOR, "#email").send_keys("newuser123@example.com")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("SecurePass!2024")
        logging.info("Entered username, email, and password.")

        terms_checkbox = driver.find_element(By.CSS_SELECTOR, "#terms")
        if not terms_checkbox.is_selected():
            terms_checkbox.click()
            logging.info("Accepted terms and conditions.")

        driver.find_element(By.CSS_SELECTOR, "#register-button").click()
        logging.info("Clicked 'Register' button.")

        confirmation_selector = "#confirmation-message"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, confirmation_selector))
        )
        confirmation_text = driver.find_element(By.CSS_SELECTOR, confirmation_selector).text
        take_screenshot(driver, "confirmation_email.png")
        logging.info(f"Confirmation message received: {confirmation_text}")

        expected_confirmation = "User account is created and confirmation email is sent"
        assert expected_confirmation in confirmation_text, \
            f"Expected confirmation not found. Actual: '{confirmation_text}'"
        logging.info("Test assertion passed: Confirmation message as expected.")

    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        take_screenshot(driver, "error_screenshot.png")
        pytest.fail(f"Test failed: {str(e)}")