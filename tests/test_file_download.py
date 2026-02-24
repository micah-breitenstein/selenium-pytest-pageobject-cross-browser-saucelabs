import logging
import pytest
import re

from pages import FileDownloadPage

log = logging.getLogger(__name__)


def test_download_links_return_200(driver, base_url):
    page = FileDownloadPage(driver, base_url=base_url).open()

    file_names = page.file_names()
    hrefs = page.file_hrefs()

    assert hrefs, "No download links found on /download"

    log.info("Found %d download files:", len(file_names))
    for name in file_names:
        log.info(" - %s", name)

    # Keep test fast — only check first 10
    to_check = hrefs[:5]

    failures = []
    for url in to_check:
        status = page.head_status(url)
        log.info("Checked %s → status %s", url, status)

        if status != 200:
            failures.append((url, status))

    assert not failures, f"Some download links did not return 200: {failures}"


PATTERN = re.compile(r"^LAKETAHOECAVEROCK_[0-9a-fA-F]{8}\.JPG$")


def test_target_file_presence_logs_only(driver, base_url):
    page = FileDownloadPage(driver, base_url=base_url).open()
    file_names = page.file_names()

    matches = [name for name in file_names if PATTERN.match(name)]

    if matches:
        log.info("✅ Matching file(s) found:")
        for m in matches:
            log.info("   - %s", m)
    else:
        log.info("⚠️ No matching files found.")

    assert True  # logging-only test