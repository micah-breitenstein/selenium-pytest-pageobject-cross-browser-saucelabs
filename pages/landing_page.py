from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage
from pages.login_page import LoginPage
from pages.checkboxes_page import CheckboxesPage
from pages.dropdown_page import DropdownPage
from pages.dynamic_loading_page import DynamicLoadingPage


class LandingPage(BasePage):
    # Links on the home page
    FORM_AUTH = (By.LINK_TEXT, "Form Authentication")
    CHECKBOXES = (By.LINK_TEXT, "Checkboxes")
    DROPDOWN = (By.LINK_TEXT, "Dropdown")
    DYNAMIC_LOADING = (By.LINK_TEXT, "Dynamic Loading")

    def load(self) -> "LandingPage":
        self.go("/")
        return self

    def go_to_login(self) -> LoginPage:
        self.click(self.FORM_AUTH)
        return LoginPage(self.driver, config=self.config)

    def go_to_checkboxes(self) -> CheckboxesPage:
        self.click(self.CHECKBOXES)
        return CheckboxesPage(self.driver, config=self.config)

    def go_to_dropdown(self) -> DropdownPage:
        self.click(self.DROPDOWN)
        return DropdownPage(self.driver, config=self.config)

    def go_to_dynamic_loading(self) -> DynamicLoadingPage:
        self.click(self.DYNAMIC_LOADING)
        return DynamicLoadingPage(self.driver, config=self.config)
