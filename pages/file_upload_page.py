# pages/file_upload_page.py

from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class FileUploadPage(BasePage):
    PATH = "/upload"

    FILE_INPUT = (By.ID, "file-upload")
    HEADER = (By.CSS_SELECTOR, "#content h3")
    UPLOADED_FILENAME = (By.ID, "uploaded-files")

    def open(self):
        self.driver.get(self.config.base_url + self.PATH)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        return self

    def upload_file(self, file_path: str | Path, upload_timeout: int = 30):
        file_path = str(Path(file_path).resolve())

        file_input = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        file_input.send_keys(file_path)

        # ✅ Safari-safe: submit the parent form of the file input
        self.driver.execute_script("arguments[0].form.submit();", file_input)

        long_wait = WebDriverWait(self.driver, upload_timeout)
        long_wait.until(EC.text_to_be_present_in_element(self.HEADER, "File Uploaded!"))
        long_wait.until(EC.visibility_of_element_located(self.UPLOADED_FILENAME))
        return self

    def upload_success_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.HEADER)).text

    def uploaded_filename(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.UPLOADED_FILENAME)).text.strip()