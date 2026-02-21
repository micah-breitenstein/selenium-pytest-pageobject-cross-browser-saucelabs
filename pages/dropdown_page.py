from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class DropdownPage:
    URL_PATH = "/dropdown"

    DROPDOWN = (By.ID, "dropdown")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_element_located(self.DROPDOWN))

    def _select(self) -> Select:
        el = self.driver.find_element(*self.DROPDOWN)
        return Select(el)

    def options_text(self) -> list[str]:
        return [o.text.strip() for o in self._select().options]

    def selected_text(self) -> str:
        return self._select().first_selected_option.text.strip()

    def select_by_visible_text(self, text: str) -> None:
        self._select().select_by_visible_text(text)

    def select_by_value(self, value: str) -> None:
        self._select().select_by_value(value)