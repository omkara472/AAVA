import pytest
import logging
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    filename='test_execution.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def load_test_cases(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        assert "testCases" in data, "Missing 'testCases' key in JSON"
        return data["testCases"]
    except Exception as e:
        logging.error(f"Failed to load test cases: {e}")
        raise

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    service = Service()
    try:
        driver = webdriver.Chrome(options=options, service=service)
        yield driver
    finally:
        driver.quit()

def execute_steps(driver, steps):
    for step in steps:
        try:
            if isinstance(step, dict):
                action = step.get("action")
                selector = step.get("selector")
                value = step.get("value")
                expected = step.get("expected")
                if action == "open_url":
                    driver.get(value)
                    logging.info(f"Opened URL: {value}")
                elif action == "input":
                    elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    elem.clear()
                    elem.send_keys(value)
                    logging.info(f"Input '{value}' into '{selector}'")
                elif action == "click":
                    elem = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    elem.click()
                    logging.info(f"Clicked element '{selector}'")
                elif action == "assert":
                    elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    assert elem.text == expected, f"Assertion failed: '{elem.text}' != '{expected}'"
                    logging.info(f"Asserted '{selector}' text equals '{expected}'")
                else:
                    logging.warning(f"Unknown action: {action}")
            else:
                logging.warning(f"Step format invalid: {step}")
        except Exception as e:
            logging.error(f"Error executing step '{step}': {e}")
            raise

def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        test_cases = load_test_cases("manual_test_cases.json")
        metafunc.parametrize("test_case", test_cases)

@pytest.mark.usefixtures("driver")
def test_manual_case(driver, test_case):
    try:
        logging.info(f"Starting test: {test_case['id']} - {test_case['title']}")
        steps = []
        for step in test_case["steps"]:
            if "Navigate" in step or "Go to" in step:
                steps.append({"action": "open_url", "value": "https://example.com/login"})
            elif "Enter" in step:
                if "username" in step:
                    steps.append({"action": "input", "selector": "#username", "value": "testuser"})
                elif "password" in step:
                    steps.append({"action": "input", "selector": "#password", "value": "password123"})
            elif "Click" in step:
                steps.append({"action": "click", "selector": "#login-button"})
            else:
                logging.warning(f"Unmapped step: {step}")
        steps.append({
            "action": "assert",
            "selector": "#welcome-message",
            "expected": test_case["expectedResult"]
        })
        execute_steps(driver, steps)
        logging.info(f"Test {test_case['id']} passed.")
    except AssertionError as ae:
        logging.error(f"Assertion failed for test {test_case['id']}: {ae}")
        pytest.fail(str(ae))
    except Exception as e:
        logging.error(f"Test {test_case['id']} failed: {e}")
        pytest.fail(str(e))
