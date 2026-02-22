from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, TypeVar, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

T = TypeVar("T")


@dataclass
class EntryAdPage:
    driver: WebDriver
    base_url: str

    # Purposeful action waits (clicks, expected appearance, etc.)
    timeout: float = 10.0

    # Short probe wait (boolean checks only)
    check_timeout: float = 1.0

    URL_PATH = "/entry_ad"

    # Locators
    _MODAL_CONTAINER = (By.ID, "modal")
    _MODAL_TITLE = (By.CSS_SELECTOR, "#modal h3")
    _MODAL_CLOSE = (By.CSS_SELECTOR, "#modal .modal-footer p")  # "Close"
    _RESTART_AD = (By.ID, "restart-ad")

    # -------------------------
    # Utilities
    # -------------------------

    def _timed(self, label: str, fn: Callable[[], T]) -> T:
        start = perf_counter()
        try:
            return fn()
        finally:
            elapsed = perf_counter() - start
            print(f"[EntryAdPage] {label}: {elapsed:.3f}s")

    def _wait(self, timeout: Optional[float] = None) -> WebDriverWait:
        t = self.timeout if timeout is None else timeout
        return WebDriverWait(self.driver, t)

    def _is_displayed(self, locator: tuple[str, str]) -> bool:
        """Freshly locate each time; avoids stale cached WebElements."""
        els = self.driver.find_elements(*locator)
        if not els:
            return False
        try:
            return els[0].is_displayed()
        except StaleElementReferenceException:
            return False

    # -------------------------
    # Page Actions
    # -------------------------

    def open(self) -> "EntryAdPage":
        self._timed(
            "open() driver.get",
            lambda: self.driver.get(self.base_url + self.URL_PATH),
        )
        return self

    def wait_for_modal(self, timeout: Optional[float] = None) -> None:
        self._timed(
            "wait_for_modal() wait for modal visible",
            lambda: self._wait(timeout).until(
                lambda d: self._is_displayed(self._MODAL_CONTAINER)
            ),
        )

    def modal_is_visible(self, timeout: Optional[float] = None) -> bool:
        t = self.check_timeout if timeout is None else timeout
        try:
            self._timed(
                f"modal_is_visible() probe (timeout={t})",
                lambda: WebDriverWait(self.driver, t).until(
                    lambda d: self._is_displayed(self._MODAL_CONTAINER)
                ),
            )
            return True
        except TimeoutException:
            print("[EntryAdPage] modal_is_visible() timed out -> False")
            return False

    def modal_title(self) -> str:
        return self._timed(
            "modal_title() find title element",
            lambda: self.driver.find_element(*self._MODAL_TITLE).text.strip(),
        )

    def close_modal(self) -> None:
        # Ensure it is visible first (fresh display check)
        self._timed(
            "close_modal() wait for modal visible",
            lambda: self._wait().until(lambda d: self._is_displayed(self._MODAL_CONTAINER)),
        )

        def _click_close():
            close_el = self._wait().until(EC.presence_of_element_located(self._MODAL_CLOSE))
            try:
                self._wait().until(EC.element_to_be_clickable(self._MODAL_CLOSE))
                close_el.click()
                return
            except (ElementClickInterceptedException, TimeoutException):
                # Fallback: JS click (very effective for this page)
                self.driver.execute_script("arguments[0].click();", close_el)

        self._timed("close_modal() click CLOSE (with JS fallback)", _click_close)

        # Robust "closed" condition:
        # treat closed as "close control no longer displayed" OR "modal container no longer displayed"
        def _closed(_driver):
            close_visible = self._is_displayed(self._MODAL_CLOSE)
            modal_visible = self._is_displayed(self._MODAL_CONTAINER)
            return (not close_visible) and (not modal_visible) or (not modal_visible) or (not close_visible)

        self._timed(
            "close_modal() wait until closed (close hidden OR modal hidden)",
            lambda: self._wait(timeout=15).until(_closed),  # a little extra room for animation
        )

    def restart_ad(self) -> None:
        self._timed(
            "restart_ad() click restart",
            lambda: self._wait().until(EC.element_to_be_clickable(self._RESTART_AD)).click(),
        )