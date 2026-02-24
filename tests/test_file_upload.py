from pathlib import Path
from pages import FileUploadPage

ORIGINAL_FILE = Path("test_file/LAKETAHOECAVEROCK.JPG")


def test_file_upload_unique_name(driver, base_url):
    page = FileUploadPage(driver, base_url).open()

    unique_name = page.upload_file_with_unique_name(ORIGINAL_FILE)

    assert page.upload_success_message() == "File Uploaded!"
    assert page.uploaded_filename() == unique_name