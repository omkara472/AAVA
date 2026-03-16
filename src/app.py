import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome WebDriver (ensure chromedriver is in PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # For CI/CD compatibility
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=options)
        yield driver
    finally:
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
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.clear()
        username_field.send_keys("valid_user")  # Replace with valid test user
        password_field.clear()
        password_field.send_keys("valid_password")  # Replace with valid test password

        # Step 3: Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Assertion: User is redirected to dashboard
        driver.implicitly_wait(5)
        try:
            dashboard = driver.find_element(By.ID, "dashboard")
            assert dashboard.is_displayed(), "Dashboard is not visible after login."
        except NoSuchElementException:
            pytest.fail("Dashboard element not found after login.")

    except WebDriverException as e:
        pytest.fail(f"WebDriver error occurred: {e}")

# requirements.txt
selenium
pytest