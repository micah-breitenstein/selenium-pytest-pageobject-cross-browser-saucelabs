from selenium.webdriver.common.by import By
from pages.core.base_page import BasePage
from pages.secure_area_page import SecureAreaPage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")

    def wait_loaded(self):
        self.wait_visible(self.USERNAME)
        return self

    def login(self, username: str, password: str) -> SecureAreaPage:
        self.wait_visible(self.USERNAME)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)

        # Safari-friendly submit
        self.driver.find_element(*self.PASSWORD).submit()

        # Confirm the next page is really loaded
        return SecureAreaPage(self.driver, self.config).wait_loaded()
    
    def login_expect_failure(self, username: str, password: str) -> "LoginPage":
        self.wait_visible(self.USERNAME)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)

        # Safari-friendly submit
        self.driver.find_element(*self.PASSWORD).submit()

        # Stay on this page; wait for the error flash to appear
        self.wait_visible(self.FLASH)
        return self
    
    def flash_message(self) -> str:
        return self.get_text(self.FLASH)
