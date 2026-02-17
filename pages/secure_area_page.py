from selenium.webdriver.common.by import By
from pages.core.base_page import BasePage


class SecureAreaPage(BasePage):
    HEADER = (By.CSS_SELECTOR, "#content h2")
    FLASH = (By.ID, "flash")

    # Unique to secure area; login page does not have /logout
    LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")

    def wait_loaded(self):
        # Best signal that we truly reached the secure area
        self.wait_visible(self.LOGOUT)
        return self

    def header(self) -> str:
        return self.get_text(self.HEADER)

    def flash_message(self) -> str:
        return self.get_text(self.FLASH)

    def logout(self) -> None:
        self.click(self.LOGOUT)
