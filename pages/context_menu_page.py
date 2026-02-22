from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException


class ContextMenuPage:
    URL_PATH = "/context_menu"
    HOT_SPOT = (By.ID, "hot-spot")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_element_located(self.HOT_SPOT))

    def context_click_hotspot(self) -> None:
        el = self.wait.until(EC.presence_of_element_located(self.HOT_SPOT))

        # Safari-friendly: dispatch a contextmenu event.
        # This reliably triggers the alert on the-internet's /context_menu page.
        try:
            self.driver.execute_script(
                """
                const el = arguments[0];
                const evt = new MouseEvent('contextmenu', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                el.dispatchEvent(evt);
                """,
                el,
            )
        except WebDriverException:
            # Fallback: works for most non-Safari browsers
            ActionChains(self.driver).context_click(el).perform()

    def wait_for_alert(self, timeout: int = 5):
        return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())

    def alert_text(self) -> str:
        alert = self.wait_for_alert()
        return alert.text.strip()

    def accept_alert(self) -> None:
        alert = self.wait_for_alert()
        alert.accept()

    def current_url(self) -> str:
        return self.driver.current_url