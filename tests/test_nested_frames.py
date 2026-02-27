from selenium.webdriver.remote.webdriver import WebDriver
from pages import NestedFramesPage


def test_nested_frames_texts(driver: WebDriver, base_url: str) -> None:
    page = NestedFramesPage(driver, base_url=base_url).open()

    assert page.left_text() == "LEFT"
    assert page.middle_text() == "MIDDLE"
    assert page.right_text() == "RIGHT"
    assert page.bottom_text() == "BOTTOM"