from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrokenImagesPage:
    URL_PATH = "/broken_images"
    IMAGES = (By.CSS_SELECTOR, "#content img")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 5):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.presence_of_all_elements_located(self.IMAGES))

    def image_srcs(self) -> list[str]:
        imgs = self.driver.find_elements(*self.IMAGES)
        srcs = []
        for img in imgs:
            src = (img.get_attribute("src") or "").strip()
            if not src:
                continue
            # sometimes src is relative; make absolute
            srcs.append(urljoin(self.base_url + "/", src))
        return srcs
