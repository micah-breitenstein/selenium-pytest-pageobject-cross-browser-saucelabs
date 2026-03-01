from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class HoversPage:
    URL_PATH = "/hovers"

    FIGURES = (By.CSS_SELECTOR, ".figure")
    AVATAR_IN_FIGURE = (By.CSS_SELECTOR, "img")
    CAPTION_IN_FIGURE = (By.CSS_SELECTOR, ".figcaption")   # <-- keep this
    NAME_IN_CAPTION = (By.CSS_SELECTOR, ".figcaption h5")
    LINK_IN_CAPTION = (By.CSS_SELECTOR, ".figcaption a")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> "HoversPage":
        self.driver.get(self.base_url + self.URL_PATH)
        return self

    def hover_user(self, user_index_1_based: int, timeout: int = 10) -> "HoversPage":
        idx = user_index_1_based - 1
        wait = WebDriverWait(self.driver, timeout)

        # Wait until the figures are present (there should be 3)
        wait.until(lambda d: len(d.find_elements(*self.FIGURES)) >= 3)

        figures = self.driver.find_elements(*self.FIGURES)
        assert 0 <= idx < len(figures), f"User index out of range: {user_index_1_based} (found {len(figures)} figures)"

        figure = figures[idx]

        # Ensure the avatar is present/visible before hovering
        avatar = figure.find_element(*self.AVATAR_IN_FIGURE)
        wait.until(lambda d: avatar.is_displayed())

        # Hover (add a tiny pause to reduce occasional “missed hover”)
        ActionChains(self.driver).move_to_element(avatar).pause(0.15).perform()

        # Wait for caption to become visible
        wait.until(lambda d: figure.find_element(*self.CAPTION_IN_FIGURE).is_displayed())

        return self

    def user_name_text(self, user_index_1_based: int) -> str:
        idx = user_index_1_based - 1
        figure = self.driver.find_elements(*self.FIGURES)[idx]
        return figure.find_element(*self.NAME_IN_CAPTION).text.strip()

    def user_profile_href(self, user_index_1_based: int) -> str:
        idx = user_index_1_based - 1
        figure = self.driver.find_elements(*self.FIGURES)[idx]
        return figure.find_element(*self.LINK_IN_CAPTION).get_attribute("href")

    def click_view_profile(self, user_index_1_based: int) -> None:
        idx = user_index_1_based - 1
        figure = self.driver.find_elements(*self.FIGURES)[idx]
        figure.find_element(*self.LINK_IN_CAPTION).click()