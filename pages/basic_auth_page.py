from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasicAuthPage:
    URL_PATH = "/basic_auth"
    MESSAGE = (By.CSS_SELECTOR, "#content p")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 5):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open_with_credentials(self, username: str, password: str):
        # Insert credentials into URL
        protocol, rest = self.base_url.split("://")
        auth_url = f"{protocol}://{username}:{password}@{rest}{self.URL_PATH}"
        self.driver.get(auth_url)

    def get_message(self) -> str:
        el = self.wait.until(
            EC.visibility_of_element_located(self.MESSAGE)
        )
        return el.text.strip()
