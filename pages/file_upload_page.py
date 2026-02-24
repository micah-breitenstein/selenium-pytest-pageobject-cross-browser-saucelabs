from __future__ import annotations

from pathlib import Path
import shutil
import uuid
import tempfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FileUploadPage:
    """
    Page object for https://the-internet.herokuapp.com/upload
    """

    PATH = "/upload"

    FILE_INPUT = (By.ID, "file-upload")
    SUBMIT_BTN = (By.ID, "file-submit")
    RESULT_HEADER = (By.TAG_NAME, "h3")
    UPLOADED_FILENAME = (By.ID, "uploaded-files")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> "FileUploadPage":
        self.driver.get(f"{self.base_url}{self.PATH}")
        return self

    # 🔥 New method: upload with unique filename
    def upload_file_with_unique_name(
        self,
        original_file: Path | str,
        upload_timeout: int = 30
    ) -> str:
        original = Path(original_file)
        if not original.exists():
            raise FileNotFoundError(f"Upload file not found: {original}")

        unique_name = f"{original.stem}_{uuid.uuid4().hex[:8]}{original.suffix}"

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir) / unique_name
            shutil.copy(original, temp_path)

            self.driver.find_element(*self.FILE_INPUT).send_keys(str(temp_path))
            self.driver.find_element(*self.SUBMIT_BTN).click()

            WebDriverWait(self.driver, upload_timeout).until(
                EC.text_to_be_present_in_element(self.RESULT_HEADER, "File Uploaded")
            )

        return unique_name

    def upload_success_message(self) -> str:
        return self.driver.find_element(*self.RESULT_HEADER).text.strip()

    def uploaded_filename(self) -> str:
        return self.driver.find_element(*self.UPLOADED_FILENAME).text.strip()