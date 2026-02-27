from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

T = TypeVar("T")


@dataclass
class NestedFramesPage:
    driver: WebDriver
    base_url: str

    PATH = "/nested_frames"
    BODY = (By.TAG_NAME, "body")
    MIDDLE_CONTENT = (By.ID, "content")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "NestedFramesPage":
        self.driver.get(self.url())
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self, timeout: int = 10) -> None:
        # frameset page: wait for expected frames by name
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.find_elements(By.NAME, "frame-top"))
        wait.until(lambda d: d.find_elements(By.NAME, "frame-bottom"))

    # ---- helpers ----
    def _in_frames(self, *frame_names: str, fn: Callable[[], T]) -> T:
        """
        Switch into a chain of frames by name, run fn(), then always return
        to default content (prevents Safari getting "stuck" in a frame).
        """
        self.driver.switch_to.default_content()
        try:
            for name in frame_names:
                self.driver.switch_to.frame(name)
            return fn()
        finally:
            self.driver.switch_to.default_content()

    def _body_text(self) -> str:
        return " ".join(self.driver.find_element(*self.BODY).text.split())

    # ---- public API ----
    def left_text(self) -> str:
        return self._in_frames("frame-top", "frame-left", fn=self._body_text)

    def middle_text(self) -> str:
        def read_middle() -> str:
            # Middle frame has <div id="content">MIDDLE</div>
            if self.driver.find_elements(*self.MIDDLE_CONTENT):
                return " ".join(self.driver.find_element(*self.MIDDLE_CONTENT).text.split())
            return self._body_text()

        return self._in_frames("frame-top", "frame-middle", fn=read_middle)

    def right_text(self) -> str:
        return self._in_frames("frame-top", "frame-right", fn=self._body_text)

    def bottom_text(self) -> str:
        return self._in_frames("frame-bottom", fn=self._body_text)