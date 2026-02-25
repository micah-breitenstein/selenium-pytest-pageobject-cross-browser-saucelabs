from __future__ import annotations

from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class ForgotPasswordPage:
    driver: WebDriver
    base_url: str

    PATH = "/forgot_password"

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    RETRIEVE_BUTTON = (By.ID, "form_submit")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "ForgotPasswordPage":
        self.driver.get(self.url())
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )

    def set_email(self, email: str) -> "ForgotPasswordPage":
        el = self.driver.find_element(*self.EMAIL_INPUT)
        el.clear()
        el.send_keys(email)
        return self

    def submit(self) -> "ForgotPasswordResultPage":
            wait = WebDriverWait(self.driver, 10)

            btn = wait.until(EC.element_to_be_clickable(self.RETRIEVE_BUTTON))

            # Normal click first
            try:
                btn.click()
            except Exception:
                # Safari can be flaky; fallback
                self.driver.execute_script("arguments[0].click();", btn)

            # Wait for a meaningful change:
            # - URL changes (expected on navigation)
            # - OR email input is gone
            # - OR success/error text appears
            def changed(d):
                url_changed = (self.PATH not in d.current_url)
                body = d.find_element(By.TAG_NAME, "body").text
                has_outcome_text = (
                    "Internal Server Error" in body
                    or "Your e-mail" in body
                    or "Your e-mail's been sent!" in body
                    or "Your e-mail’s been sent!" in body
                )
                try:
                    d.find_element(*self.EMAIL_INPUT)
                    email_still_there = True
                except Exception:
                    email_still_there = False

                return url_changed or has_outcome_text or (not email_still_there)

            try:
                wait.until(changed)
            except TimeoutException:
                # If it never changes, we still return the result wrapper (test will show body text)
                pass

            return ForgotPasswordResultPage(self.driver)

    def retrieve_password(self, email: str) -> "ForgotPasswordResultPage":
        return self.set_email(email).submit()


class ForgotPasswordResultPage:
    """
    The Internet site *used to* show a success message.
    Lately it may show 'Internal Server Error' (500-style error page).

    This wrapper makes assertions easy without relying on fragile structure.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def body_text(self) -> str:
        return self.driver.find_element(By.TAG_NAME, "body").text

    def is_internal_server_error(self) -> bool:
        return "Internal Server Error" in self.body_text()

    def is_success_message(self) -> bool:
        # historical behavior
        text = self.body_text()
        return "Your e-mail's been sent!" in text or "Your e-mail’s been sent!" in text