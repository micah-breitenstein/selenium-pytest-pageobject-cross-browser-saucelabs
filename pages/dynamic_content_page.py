from selenium.webdriver.common.by import By
from pages.core.base_page import BasePage


class DynamicContentPage(BasePage):
    URL_PATH = "/dynamic_content"
    ALL_ROWS = (By.CSS_SELECTOR, "#content .row")
    ROW_TEXT = (By.CSS_SELECTOR, ".large-10")
    ROW_IMAGE = (By.CSS_SELECTOR, ".large-2 img")

    def open_page(self, static: bool = False) -> None:
        url = f"{self.config.base_url}{self.URL_PATH}"
        if static:
            url += "?with_content=static"
        self.driver.get(url)
        self.wait_visible(self.ALL_ROWS)

    def rows(self):
        return self.find_all(self.ALL_ROWS)

    def rows_text(self) -> list[str]:
        rows = self.rows()
        texts = []
        for r in rows:
            els = r.find_elements(*self.ROW_TEXT)
            if els:
                t = els[0].text.strip()
                if t:
                    texts.append(t)
        return texts

    def rows_image_src(self) -> list[str]:
        rows = self.rows()
        srcs = []
        for r in rows:
            imgs = r.find_elements(*self.ROW_IMAGE)
            if imgs:
                srcs.append(imgs[0].get_attribute("src") or "")
        return srcs

    def refresh(self) -> None:
        self.driver.refresh()
        self.wait_visible(self.ALL_ROWS)

    def row_count(self) -> int:
        return len(self.rows_text())    