import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChallengingDomPage:
    URL_PATH = "/challenging_dom"
    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    
    BLUE_BTN = (By.CSS_SELECTOR, "a.button:not(.alert):not(.success)")
    RED_BTN = (By.CSS_SELECTOR, "a.button.alert")
    GREEN_BTN = (By.CSS_SELECTOR, "a.button.success")

    CANVAS = (By.CSS_SELECTOR, "canvas")  # the <canvas> element (no id on page)

    def canvas_data_url(self) -> str:
        canvas = self.driver.find_element(*self.CANVAS)
        return self.driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)
    
    def wait_for_canvas_change(self, before: str, timeout: int = 5) -> str:
        wait = WebDriverWait(self.driver, timeout)

        def changed(d):
            after = self.canvas_data_url()
            return after if after and after != before else False

        return wait.until(changed)

    def wait_for_answer_to_change(self, before: str, timeout: int = 5) -> str:
        wait = WebDriverWait(self.driver, timeout)
        def changed(d):
            after = self.answer_value()
            return after if after and after != before else False
        return wait.until(changed)

    def answer_value(self) -> str:
        # The "Answer" is drawn into the canvas, so we fingerprint the canvas pixels
        data_url = self.canvas_data_url()
        if not data_url:
            return ""
        return hashlib.sha256(data_url.encode("utf-8")).hexdigest()

    def button_texts(self) -> dict[str, str]:
        return {
            "blue": self.driver.find_element(*self.BLUE_BTN).text.strip(),
            "red": self.driver.find_element(*self.RED_BTN).text.strip(),
            "green": self.driver.find_element(*self.GREEN_BTN).text.strip(),
        }

    def click_button(self, color: str) -> None:
        mapping = {"blue": self.BLUE_BTN, "red": self.RED_BTN, "green": self.GREEN_BTN}
        try:
            locator = mapping[color.lower().strip()]
        except KeyError:
            raise ValueError("color must be one of: blue, red, green")
        self.driver.find_element(*locator).click()
        
    def wait_for_button_texts_to_change(self, before: dict[str, str], timeout: int = 5) -> dict[str, str]:
        wait = WebDriverWait(self.driver, timeout)

        def changed(d):
            after = self.button_texts()
            return after if after != before else False

        return wait.until(changed)

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_all_elements_located(self.TABLE_ROWS))

    def rows(self):
        return self.driver.find_elements(*self.TABLE_ROWS)

    def click_delete_by_column_text(self, column_index: int, expected_text: str) -> None:
        """
        column_index is 0-based
        """
        for row in self.rows():
            cells = row.find_elements(By.TAG_NAME, "td")

            if column_index >= len(cells):
                continue

            cell_text = cells[column_index].text.strip()

            if expected_text in cell_text:
                row.find_element(By.LINK_TEXT, "delete").click()
                return

        raise AssertionError(
            f"No row found where column {column_index} contains '{expected_text}'"
        )

    def current_url(self) -> str:
        return self.driver.current_url
