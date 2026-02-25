from __future__ import annotations

from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class IFramePage:
    driver: WebDriver
    base_url: str

    PATH = "/iframe"

    IFRAME = (By.ID, "mce_0_ifr")
    EDITOR_BODY = (By.ID, "tinymce")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "IFramePage":
        self.driver.get(self.url())
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.IFRAME)
        )

    def switch_to_editor(self) -> None:
        iframe = self.driver.find_element(*self.IFRAME)
        self.driver.switch_to.frame(iframe)

    def switch_to_default(self) -> None:
        self.driver.switch_to.default_content()

    def get_editor_text(self) -> str:
        self.switch_to_editor()
        text = self.driver.find_element(*self.EDITOR_BODY).text
        self.switch_to_default()
        return text

    def set_editor_text(self, text: str) -> None:
        self.switch_to_editor()
        body = self.driver.find_element(*self.EDITOR_BODY)
        body.clear()
        body.send_keys(text)
        self.switch_to_default()