import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # For CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://demo.opencart.com")

    yield driver
    driver.quit()


# Test Case 1: Verify Homepage Title
def test_homepage_title(driver):
    assert "Your Store" in driver.title


# Test Case 2: Search Product
def test_search_product(driver):
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys("MacBook")

    search_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    search_button.click()

    time.sleep(2)

    product = driver.find_element(By.LINK_TEXT, "MacBook")
    assert product.is_displayed()


# Test Case 3: Add Product to Cart
def test_add_to_cart(driver):
    driver.find_element(By.LINK_TEXT, "MacBook").click()

    add_to_cart_button = driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()

    time.sleep(2)

    success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success")
    assert "Success" in success_message.text


# Test Case 4: Verify Cart Button
def test_cart_button(driver):
    cart = driver.find_element(By.ID, "cart-total")
    assert cart.is_displayed()"
}