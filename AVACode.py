# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects, provides common Selenium operations."""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, by, locator):
        """Wait for element to be present and return it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def click(self, by, locator):
        """Wait for element to be clickable and click it."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def type(self, by, locator, value, clear=True):
        """Type into an input after waiting for it."""
        element = self.find(by, locator)
        if clear:
            element.clear()
        element.send_keys(value)

    def is_visible(self, by, locator):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except:
            return False

    def get_text(self, by, locator):
        """Get text from an element."""
        element = self.find(by, locator)
        return element.text

    def wait_for_url(self, url_fragment):
        """Wait until URL contains given fragment."""
        WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(url_fragment)
        )
