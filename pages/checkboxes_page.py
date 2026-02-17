from selenium.webdriver.common.by import By
from pages.core.base_page import BasePage


class CheckboxesPage(BasePage):
    CB1 = (By.CSS_SELECTOR, "#checkboxes input:nth-of-type(1)")
    CB2 = (By.CSS_SELECTOR, "#checkboxes input:nth-of-type(2)")

    def is_checked(self, locator) -> bool:
        el = self.wait_visible(locator)
        return el.is_selected()

    def set_checked(self, locator, checked: bool) -> None:
        el = self.wait_visible(locator)
        if el.is_selected() != checked:
            el.click()
