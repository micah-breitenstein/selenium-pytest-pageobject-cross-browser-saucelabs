from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DisappearingElementsPage:
    URL_PATH = "/disappearing_elements"

    MENU_LINKS = (By.CSS_SELECTOR, "ul li a")   # left menu
    # Safer: look up by visible text
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_all_elements_located(self.MENU_LINKS))

    def menu_texts(self) -> list[str]:
        return [el.text.strip() for el in self.driver.find_elements(*self.MENU_LINKS) if el.text.strip()]

    def has_menu_item(self, label: str) -> bool:
        return label in self.menu_texts()

    def refresh(self) -> None:
        self.driver.refresh()
        self.wait.until(EC.presence_of_all_elements_located(self.MENU_LINKS))