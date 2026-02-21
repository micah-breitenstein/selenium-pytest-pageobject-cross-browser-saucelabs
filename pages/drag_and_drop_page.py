from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DragAndDropPage:
    URL_PATH = "/drag_and_drop"

    COLUMN_A = (By.ID, "column-a")
    COLUMN_B = (By.ID, "column-b")
    HEADER_A = (By.CSS_SELECTOR, "#column-a header")
    HEADER_B = (By.CSS_SELECTOR, "#column-b header")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_element_located(self.COLUMN_A))
        self.wait.until(EC.presence_of_element_located(self.COLUMN_B))

    def header_texts(self) -> tuple[str, str]:
        a = self.driver.find_element(*self.HEADER_A).text.strip()
        b = self.driver.find_element(*self.HEADER_B).text.strip()
        return a, b

    def swap_columns_html5(self) -> None:
        before = self.header_texts()

        left = self.driver.find_element(*self.COLUMN_A)   # left column container
        right = self.driver.find_element(*self.COLUMN_B)  # right column container

        self.driver.execute_script(
            """
            const src = arguments[0];
            const dst = arguments[1];
            const dataTransfer = new DataTransfer();

            function fire(type, elem) {
            const evt = new DragEvent(type, { bubbles: true, cancelable: true, dataTransfer });
            return elem.dispatchEvent(evt);
            }

            fire('dragstart', src);
            fire('dragenter', dst);
            fire('dragover', dst);
            fire('drop', dst);
            fire('dragend', src);
            """,
            left, right
        )

        # Wait until the headers swap relative to before
        self.wait.until(lambda d: self.header_texts() == (before[1], before[0]))

    def current_url(self) -> str:
        return self.driver.current_url