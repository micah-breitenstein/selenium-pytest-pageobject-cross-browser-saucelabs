from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AddRemoveElementsPage:
    URL_PATH = "/add_remove_elements/"
    ADD_BUTTON = (By.CSS_SELECTOR, "button[onclick='addElement()']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.added-manually")  # all "Delete" buttons

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 5):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.visibility_of_element_located(self.ADD_BUTTON))

    def add_element(self, times: int = 1) -> None:
        add = self.driver.find_element(*self.ADD_BUTTON)
        for _ in range(times):
            add.click()

    def delete_count(self) -> int:
        return len(self.driver.find_elements(*self.DELETE_BUTTONS))

    def wait_for_delete_count(self, expected: int) -> None:
        self.wait.until(lambda d: len(d.find_elements(*self.DELETE_BUTTONS)) == expected)

    def click_delete_at_index(self, index: int = 0) -> None:
        buttons = self.driver.find_elements(*self.DELETE_BUTTONS)
        if index < 0 or index >= len(buttons):
            raise IndexError(f"Delete button index {index} out of range (count={len(buttons)})")
        buttons[index].click()
