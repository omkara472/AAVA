from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    """

    # Placeholder selectors: Update with actual selectors for your application.
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='error']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_BUTTON = (By.ID, "submitBtn")
    SUCCESS_RESET_MESSAGE = (By.XPATH, "//div[contains(text(), 'Password reset link sent')]")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def go_to(self):
        """
        Navigates to the login page.
        """
        self.driver.get(f"{self.base_url}/login")

    def login(self, username, password):
        """
        Performs login action.
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """
        Retrieves error message displayed on login failure.
        """
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text

    def click_forgot_password(self):
        """
        Clicks the 'Forgot Password' link.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)
        ).click()

    def reset_password(self, email):
        """
        Submits password reset request.
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        ).send_keys(email)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_reset_success_message(self):
        """
        Retrieves the password reset success message.
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_RESET_MESSAGE)
        ).text
