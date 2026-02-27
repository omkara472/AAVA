import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# --------------------------------------------------
# Fixture (Driver Setup)
# --------------------------------------------------
@pytest.fixture(scope="function")
def driver():

    chrome_options = Options()

    # ✅ Needed for GitHub Actions / CI
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.maximize_window()
    yield driver
    driver.quit()


# --------------------------------------------------
# Test Case 1
# --------------------------------------------------
def test_google_title(driver):

    driver.get("https://www.google.com")

    assert "Google" in driver.title


# --------------------------------------------------
# Test Case 2
# --------------------------------------------------
def test_google_search_box_present(driver):

    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")

    assert search_box.is_displayed()