from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects."""

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
        return element

    def enter_text(self, by, locator, text):
        """Clear and enter text into input field."""
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)
        return element

    def is_visible(self, by, locator):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False

    def get_text(self, by, locator):
        """Get text of an element."""
        element = self.find(by, locator)
        return element.text

# Additional modular code omitted for brevity, see full context for all files
