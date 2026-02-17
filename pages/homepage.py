from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    URL = "https://example.com"

    # Locators
    HEADING = (By.TAG_NAME, "h1")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def get_heading_text(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.HEADING)
        )
        return element.text
