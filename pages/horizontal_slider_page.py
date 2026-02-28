from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class HorizontalSliderPage:
    URL_PATH = "/horizontal_slider"

    SLIDER = (By.CSS_SELECTOR, "input[type='range']")
    VALUE = (By.ID, "range")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    # -------------------------
    # Navigation
    # -------------------------
    def open(self) -> "HorizontalSliderPage":
        self.driver.get(self.base_url + self.URL_PATH)
        return self

    # -------------------------
    # Value helpers
    # -------------------------
    def value_text(self) -> str:
        return self.driver.find_element(*self.VALUE).text.strip()

    def value_float(self) -> float:
        return float(self.value_text())

    # -------------------------
    # Public API
    # -------------------------
    def set_to(self, target: float, timeout: int = 10) -> "HorizontalSliderPage":
        """
        Sets slider value in a cross-browser safe way.
        Safari uses JS fallback automatically.
        """

        browser = self.driver.capabilities.get("browserName", "").lower()

        if "safari" in browser:
            return self._set_with_js(target, timeout)

        return self._set_with_arrows(target, timeout)

    # -------------------------
    # Arrow key strategy
    # -------------------------
    def _set_with_arrows(self, target: float, timeout: int):
        slider = self.driver.find_element(*self.SLIDER)
        slider.click()

        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: self.value_text() != "")

        max_moves = 60

        for _ in range(max_moves):
            current = self.value_float()

            if current == target:
                return self

            if current < target:
                slider.send_keys(Keys.ARROW_RIGHT)
            else:
                slider.send_keys(Keys.ARROW_LEFT)

            wait.until(lambda d: float(d.find_element(*self.VALUE).text) != current)

        raise AssertionError(f"Could not reach target {target}")

    # -------------------------
    # Safari-safe JS strategy
    # -------------------------
    def _set_with_js(self, target: float, timeout: int):
        slider = self.driver.find_element(*self.SLIDER)

        self.driver.execute_script(
            """
            const el = arguments[0];
            const val = arguments[1];
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            slider,
            str(target),
        )

        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self.VALUE).text.strip() == str(target)
        )

        return self