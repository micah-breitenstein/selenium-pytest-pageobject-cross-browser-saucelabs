from selenium.webdriver.common.by import By
from pages.core.base_page import BasePage


class DynamicContentPage(BasePage):
    URL_PATH = "/dynamic_content"

    ALL_ROWS = (By.CSS_SELECTOR, "#content .row")
    ROW_IMAGE = (By.CSS_SELECTOR, ".large-2 img")
    ROW_TEXT = (By.CSS_SELECTOR, ".large-10")

    def open_page(self) -> None:
        self.driver.get(f"{self.config.base_url}{self.URL_PATH}")
        self.wait_visible(self.ALL_ROWS)

    def rows(self):
        rows = self.find_all(self.ALL_ROWS)

        dyn = []
        for r in rows:
            # Must have the text container
            text_els = r.find_elements(*self.ROW_TEXT)
            if not text_els:
                continue

            txt = text_els[0].text.strip()
            if not txt:
                continue  # skip layout/empty rows

            dyn.append(r)

        self.log.info(f"ALL_ROWS={len(rows)} DYNAMIC_ROWS={len(dyn)}")
        return dyn

    def row_count(self) -> int:
        return len(self.rows())

    def rows_text(self) -> list[str]:
        return [r.find_element(*self.ROW_TEXT).text.strip() for r in self.rows()]

    def refresh(self) -> None:
        self.driver.refresh()
        self.wait_visible(self.ALL_ROWS)