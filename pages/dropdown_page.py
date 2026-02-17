from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.core.base_page import BasePage


class DropdownPage(BasePage):
    DROPDOWN = (By.ID, "dropdown")

    def select_by_visible_text(self, text: str) -> None:
        el = self.wait_visible(self.DROPDOWN)
        Select(el).select_by_visible_text(text)

    def selected_text(self) -> str:
        el = self.wait_visible(self.DROPDOWN)
        return Select(el).first_selected_option.text