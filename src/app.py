import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


# ==========================================
# Setup & Teardown (Inside Same File)
# ==========================================
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Comment below line if you want to see browser
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


# ==========================================
# Test Case 1: Verify Google Title
# ==========================================
def test_verify_google_title(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title


# ==========================================
# Test Case 2: Google Search Functionality
# ==========================================
def test_google_search(driver):
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("PyTest Selenium")
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)  # For demo only (avoid in real frameworks)

    assert "PyTest Selenium" in driver.title


# ==========================================
# Test Case 3: Verify Example.com Page
# ==========================================
def test_example_page_title(driver):
    driver.get("https://example.com")
    assert "Example Domain" in driver.title


# ==========================================
# Test Case 4: Parametrized Search Test
# ==========================================
@pytest.mark.parametrize("search_term", [
    "Python",
    "Automation",
    "Testing",
    "Selenium"
])
def test_multiple_google_search(driver, search_term):
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    assert search_term in driver.title


# ==========================================
# Test Case 5: Negative Test (Intentional Fail Example)
# ==========================================
def test_negative_title_validation(driver):
    driver.get("https://example.com")
    assert "Google" not in driver.title