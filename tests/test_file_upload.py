from pathlib import Path
import pytest
from pages import FileUploadPage


TEST_ASSET = Path("test_file/LAKETAHOECAVEROCK.JPG")


def test_file_upload_jpg(driver, base_url):
    if not TEST_ASSET.exists():
        pytest.skip(f"Test asset not found: {TEST_ASSET}")

    page = FileUploadPage(driver, base_url=base_url).open()
    page.upload_file(TEST_ASSET, upload_timeout=60)

    assert page.upload_success_message() == "File Uploaded!"
    assert page.uploaded_filename() == TEST_ASSET.name