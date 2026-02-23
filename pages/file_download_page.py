# pages/file_download_page.py
from __future__ import annotations

from urllib.parse import urljoin

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.core.base_page import BasePage


class FileDownloadPage(BasePage):
    PATH = "/download"

    FILE_LINKS = (By.CSS_SELECTOR, "#content a")

    def open(self) -> "FileDownloadPage":
        self.driver.get(self.config.base_url + self.PATH)
        # Ensure DOM is ready (prevents occasional race)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.wait.until(EC.presence_of_all_elements_located(self.FILE_LINKS))
        return self

    def file_hrefs(self) -> list[str]:
        """Return absolute URLs for each download link on the page."""
        links = self.driver.find_elements(*self.FILE_LINKS)
        hrefs: list[str] = []
        for a in links:
            href = (a.get_attribute("href") or "").strip()
            if not href:
                continue
            # Normalize relative -> absolute just in case
            hrefs.append(urljoin(self.config.base_url + "/", href))
        return hrefs

    def file_names(self) -> list[str]:
        links = self.driver.find_elements(*self.FILE_LINKS)
        return [(a.text or "").strip() for a in links if (a.text or "").strip()]

    def head_status(self, url: str, timeout: int = 15) -> int:
        """
        Try HEAD first (cheap). Some servers don't support HEAD; fall back to GET.
        """
        try:
            r = requests.head(url, allow_redirects=True, timeout=timeout)
            # Some servers reply 405 for HEAD; treat as "try GET"
            if r.status_code in (405, 501):
                raise RuntimeError("HEAD not supported")
            return r.status_code
        except Exception:
            r = requests.get(url, stream=True, allow_redirects=True, timeout=timeout)
            try:
                return r.status_code
            finally:
                r.close()