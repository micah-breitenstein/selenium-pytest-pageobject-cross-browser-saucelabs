from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FloatingMenuPage:
    PATH = "/floating_menu"

    MENU = (By.ID, "menu")
    MENU_LINKS = (By.CSS_SELECTOR, "#menu a")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> "FloatingMenuPage":
        self.driver.get(f"{self.base_url}{self.PATH}")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MENU))
        return self

    def menu_is_displayed(self) -> bool:
        return self.driver.find_element(*self.MENU).is_displayed()

    def scroll_by(self, pixels: int) -> None:
        # Safari-safe scroll
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", pixels)

    def click_menu_item(self, text: str) -> None:
        links = self.driver.find_elements(*self.MENU_LINKS)
        for a in links:
            if a.text.strip().lower() == text.strip().lower():
                a.click()
                return
        raise AssertionError(f"Menu item not found: {text!r}")

    def current_hash(self) -> str:
        return self.driver.execute_script("return window.location.hash;") or ""