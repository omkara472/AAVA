import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome options for CI/CD compatibility (headless, no GPU)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_verify_login_functionality(driver):
    """
    Test Case ID: SCRUM-6
    Title: Verify login functionality
    Description: Ensure user can log in with valid credentials
    Tags: login, authentication
    Attachments: screenshot1.png
    """
    try:
        # Step 1: Navigate to login page
        driver.get("https://example.com/login")
        
        # Step 2: Enter valid username and password
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        username_field.clear()
        username_field.send_keys("valid_username")  # Replace with actual test data
        password_field.clear()
        password_field.send_keys("valid_password")  # Replace with actual test data
        
        # Step 3: Click login button
        login_button = driver.find_element(By.ID, "login")
        login_button.click()
        
        # Assertion: User is redirected to dashboard
        # Wait for dashboard element to appear
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        dashboard = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "dashboard"))
        )
        assert dashboard.is_displayed(), "Dashboard not visible after login"
        
        # Optionally, take screenshot for attachments
        driver.save_screenshot("screenshot1.png")
        
    except Exception as e:
        # Log error for CI/CD traceability
        import logging
        logging.basicConfig(level=logging.INFO)
        logging.error(f"Test SCRUM-6 failed: {e}")
        raise

requirements.txt:
selenium
pytest
pytest-xdist
webdriver-manager
