from selenium.webdriver.common.by import By

class FlashMessage:
    FLASH = (By.ID, "flash")

    def __init__(self, page):
        self.page = page

    def text(self) -> str:
        return self.page.get_text(self.FLASH)
