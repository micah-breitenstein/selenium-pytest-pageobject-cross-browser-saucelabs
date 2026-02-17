from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class DynamicLoadingPage(BasePage):
    EXAMPLE_2 = (By.PARTIAL_LINK_TEXT, "Example 2")
    START_BTN = (By.CSS_SELECTOR, "#start button")
    LOADING = (By.ID, "loading")
    FINISH = (By.ID, "finish")

    def open_example_2(self) -> "DynamicLoadingPage":
        self.click(self.EXAMPLE_2)
        return self

    def start_loading(self) -> "DynamicLoadingPage":
        self.click(self.START_BTN)
        self.wait_invisible(self.LOADING)
        self.wait_visible(self.FINISH)
        return self

    def finish_text(self) -> str:
        # The "Hello World!" text lives inside #finish
        return self.get_text(self.FINISH)
