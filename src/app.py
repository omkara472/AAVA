# test_jira_cases.py
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(filename='test_execution.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def wait_for_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except Exception as e:
        logging.error(f"Element with selector '{selector}' not found: {e}")
        raise

@pytest.mark.parametrize("test_case", [
    {
        "id": "SCRUM-6",
        "title": "Verify login functionality",
        "description": "Ensure user can log in with valid credentials",
        "steps": [
            {"action": "open_url", "value": "https://example.com/login"},
            {"action": "input", "selector": "#username", "value": "testuser"},
            {"action": "input", "selector": "#password", "value": "password123"},
            {"action": "click", "selector": "#login-button"},
            {"action": "assert", "selector": "#dashboard", "expected": "Dashboard"}
        ],
        "expectedResult": "User is redirected to dashboard",
        "tags": ["login", "authentication"],
        "attachments": ["screenshot1.png"]
    },
    {
        "id": "SCRUM-7",
        "title": "Validate password reset",
        "description": "Check password reset functionality",
        "steps": [
            {"action": "open_url", "value": "https://example.com/login"},
            {"action": "click", "selector": "#forgot-password"},
            {"action": "input", "selector": "#email", "value": "user@example.com"},
            {"action": "click", "selector": "#reset-submit"},
            {"action": "assert", "selector": "#notification", "expected": "Password reset email is sent"}
        ],
        "expectedResult": "Password reset email is sent",
        "tags": ["password", "reset"],
        "attachments": []
    }
])
def test_jira_case(driver, test_case):
    logging.info(f"Executing Test Case: {test_case['id']} - {test_case['title']}")
    try:
        for step in test_case['steps']:
            action = step.get('action')
            if action == 'open_url':
                driver.get(step['value'])
                logging.info(f"Opened URL: {step['value']}")
            elif action == 'input':
                element = wait_for_element(driver, step['selector'])
                element.clear()
                element.send_keys(step['value'])
                logging.info(f"Input '{step['value']}' into '{step['selector']}'")
            elif action == 'click':
                element = wait_for_element(driver, step['selector'])
                element.click()
                logging.info(f"Clicked element '{step['selector']}'")
            elif action == 'assert':
                element = wait_for_element(driver, step['selector'])
                actual = element.text.strip()
                expected = step['expected']
                assert actual == expected, \
                    f"Assertion failed for '{step['selector']}': expected '{expected}', got '{actual}'"
                logging.info(f"Asserted '{step['selector']}' text is '{expected}'")
            else:
                logging.warning(f"Unknown action '{action}' in step: {step}")
        logging.info(f"Test Case '{test_case['id']}' PASSED")
    except AssertionError as ae:
        logging.error(f"Test Case '{test_case['id']}' FAILED: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Test Case '{test_case['id']}' ERROR: {e}")
        pytest.fail(str(e))
