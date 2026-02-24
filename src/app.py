# tests/test_scrum_login.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os


logging.basicConfig(
    filename="test_scrum_login.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


def test_scrum_6_login_functionality(driver):

    login_url = "https://example.com/login"
    driver.get(login_url)

    username_selector = "#username"
    password_selector = "#password"
    login_button_selector = "#login-button"
    dashboard_selector = "#dashboard"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
    ).send_keys("valid_user")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))
    ).send_keys("valid_password")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector))
    ).click()

    dashboard_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, dashboard_selector))
    )

    assert "Dashboard" in dashboard_element.text or "Welcome" in dashboard_element.text

    driver.save_screenshot("screenshot1.png")
