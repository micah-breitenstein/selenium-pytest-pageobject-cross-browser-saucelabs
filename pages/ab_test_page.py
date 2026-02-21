from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class ABTestPage:
    URL_PATH = "/abtest"
    HEADER = (By.CSS_SELECTOR, "h3")

    # include all known headings you might see across versions/forks
    ALLOWED_HEADERS = {
        "No A/B Test",
        "A/B Test Variation 1",
        "A/B Test Control",
    }

    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")

    def header_text(self) -> str:
        return self.driver.find_element(*self.HEADER).text.strip()

    def assert_header_is_valid(self) -> None:
        actual = self.header_text()
        assert actual in self.ALLOWED_HEADERS, (
            f"Unexpected header '{actual}'. Expected one of: {sorted(self.ALLOWED_HEADERS)}"
        )
