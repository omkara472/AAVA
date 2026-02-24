# jira_config.json: {"url": "https://omkarmareedu472.atlassian.net/", "token": "ATATT3xFfGF0z9PCEhW8KIQBPlU12tlHSTNcKn-RttISCJ9Th9zYJWbanLEIJNGEFRrq4VvupezRm8F4O2ILlb0hQMv0zWbmqiKQzFq47vQ3abaj23J3ikeUh-Q-kxfWPfHGIrs48v-yvK0_33ITs_svejbCy6scv6r55bfwDbxW8kBdcM6y7C8=074E7834", "user": "omkarmareedu472@gmail.com", "board": "SCRUM", "ticketid": "SCRUM-6"}
# export_settings.json: {"outputFormat": "JSON", "schemaVersion": "1.0", "exportPath": "./exports/"}
# exports/testcases.json: {"testCases": [{"id": "SCRUM-6", "title": "Verify login functionality", "description": "Ensure user can log in with valid credentials", "steps": ["Navigate to login page", "Enter valid username and password", "Click login button"], "expectedResult": "User is redirected to dashboard", "tags": ["login", "authentication"], "attachments": ["screenshot1.png"]}]}
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
def take_screenshot(driver, name):
    attachments_dir = './attachments'
    os.makedirs(attachments_dir, exist_ok=True)
    path = os.path.join(attachments_dir, name)
    driver.save_screenshot(path)
def test_login_functionality(driver):
    login_url = "https://example.com/login"
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
    username = "testuser"
    password = "password123"
    driver.find_element(By.CSS_SELECTOR, "#username").clear()
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "#password").clear()
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#login-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dashboard")))
    welcome_message = driver.find_element(By.CSS_SELECTOR, "#welcome-message").text
    assert welcome_message == "Welcome, testuser!"
    take_screenshot(driver, "screenshot1.png")