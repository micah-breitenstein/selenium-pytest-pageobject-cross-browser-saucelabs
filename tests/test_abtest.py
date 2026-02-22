import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import ABTestPage


@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,800")
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(2)
    yield d
    d.quit()


def test_abtest_header(driver, base_url):
    page = ABTestPage(driver, base_url)
    page.open()
    page.assert_header_is_valid()
