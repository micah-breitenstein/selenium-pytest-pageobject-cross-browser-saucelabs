from __future__ import annotations

import time
import logging

from dataclasses import dataclass
from urllib.parse import urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass(frozen=True)
class Config:
    base_url: str
    timeout: int = 10


class BasePage:
    def __init__(
        self,
        driver,
        config: Config | None = None,
        *,
        base_url: str | None = None,
        timeout: int = 10,
    ):
        """
        Supports:
            BasePage(driver, base_url="http://127.0.0.1:9292")
            BasePage(driver, config=Config(...))
        """

        self.driver = driver
        self.log = logging.getLogger(self.__class__.__name__)

        # Build config safely at runtime (never as default argument)
        if config is None:
            if base_url is None:
                # Fallback default (safe)
                base_url = "https://the-internet.herokuapp.com"
            config = Config(base_url=base_url.rstrip("/"), timeout=timeout)
        else:
            # Allow explicit base_url override even if config passed
            if base_url is not None:
                config = Config(
                    base_url=base_url.rstrip("/"),
                    timeout=config.timeout,
                )

        self.config = config
        self.wait = WebDriverWait(driver, self.config.timeout)

    # -------------------------
    # Navigation
    # -------------------------
    def go(self, path: str) -> None:
        url = urljoin(self.config.base_url + "/", path.lstrip("/"))
        self.log.info(f"GO → {url}")
        self.driver.get(url)

    # -------------------------
    # Wait Helpers
    # -------------------------
    def wait_visible(self, locator):
        self.log.info(f"WAIT visible → {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        self.log.info(f"WAIT clickable → {locator}")
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator):
        self.log.info(f"WAIT invisible → {locator}")
        return self.wait.until(EC.invisibility_of_element_located(locator))

    # -------------------------
    # Actions
    # -------------------------
    def click(self, locator) -> None:
        self.log.info(f"CLICK → {locator}")
        self.wait_clickable(locator).click()

    def type(self, locator, text: str, clear: bool = True) -> None:
        # Redact likely passwords
        redacted = "***" if "password" in str(locator).lower() else text
        self.log.info(f"TYPE → {locator} value={redacted!r} clear={clear}")

        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator) -> str:
        self.log.info(f"GET_TEXT → {locator}")
        return self.wait_visible(locator).text

    def is_visible(self, locator, timeout=1):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.log.info(f"VISIBLE ✓ {locator}")
            return True
        except Exception:
            self.log.info(f"NOT VISIBLE ✗ {locator}")
            return False

    def wait_any(self, locator_a, locator_b, timeout=10):
        """
        Wait until either locator_a or locator_b is visible.
        Returns "first" if locator_a wins, "second" if locator_b wins.
        """
        self.log.info(f"WAIT_ANY → {locator_a} OR {locator_b} timeout={timeout}s")

        end = time.time() + timeout
        while time.time() < end:
            if self.is_visible(locator_a, timeout=0.2):
                self.log.info("WAIT_ANY result → first")
                return "first"
            if self.is_visible(locator_b, timeout=0.2):
                self.log.info("WAIT_ANY result → second")
                return "second"

        self.log.error("WAIT_ANY timed out")
        raise TimeoutError(f"Neither locator became visible within {timeout}s")
    
    def go(self, path: str) -> None:
        url = urljoin(self.config.base_url + "/", path.lstrip("/"))
        self.log.info(f"BASE_URL = {self.config.base_url}")
        self.log.info(f"GO → {url}")
        self.driver.get(url)
