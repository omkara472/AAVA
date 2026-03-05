from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://demo.opencart.com")
driver.find_element(By.NAME, "search").send_keys("MacBook")
print(driver.title)
driver.quit()