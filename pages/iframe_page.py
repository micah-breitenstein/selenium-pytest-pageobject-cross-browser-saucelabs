from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    # -----------------
    # Frame switching
    # -----------------

    def _switch_to_editor(self) -> None:
        iframe = self.driver.find_element(*self.IFRAME)
        self.driver.switch_to.frame(iframe)

    def _switch_to_default(self) -> None:
        self.driver.switch_to.default_content()

    # -----------------
    # State detection
    # -----------------

    def is_editor_editable(self) -> bool:
        """
        Returns True if the TinyMCE body is editable.
        """
        self._switch_to_editor()
        try:
            body = self.driver.find_element(*self.EDITOR_BODY)
            content_editable = body.get_attribute("contenteditable")
            return (content_editable or "").lower() == "true"
        finally:
            self._switch_to_default()

    def is_read_only_message_present(self) -> bool:
        """
        Detects TinyMCE read-only / quota exhaustion message.
        """
        self._switch_to_editor()
        try:
            text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            return (
                "read-only mode" in text
                or "no more editor loads" in text
                or "quota" in text
            )
        finally:
            self._switch_to_default()

    # -----------------
    # Editor interaction
    # -----------------

    def get_editor_text(self) -> str:
        self._switch_to_editor()
        try:
            text = self.driver.find_element(*self.EDITOR_BODY).text
            return " ".join(text.split())
        finally:
            self._switch_to_default()

    def set_editor_text(self, text: str) -> None:
        """
        Safely updates editor text if editable.
        Raises RuntimeError if editor is read-only.
        """
        if not self.is_editor_editable() or self.is_read_only_message_present():
            raise RuntimeError("TinyMCE editor is in read-only mode.")

        self._switch_to_editor()
        try:
            body = self.driver.find_element(*self.EDITOR_BODY)
            body.click()

            # Do NOT use clear() — Safari + contenteditable bug
            body.send_keys(Keys.COMMAND, "a")
            body.send_keys(Keys.DELETE)
            body.send_keys(text)

        finally:
            self._switch_to_default()

    def is_read_only(self) -> bool:
        return self.is_read_only_message_present() or (not self.is_editor_editable())