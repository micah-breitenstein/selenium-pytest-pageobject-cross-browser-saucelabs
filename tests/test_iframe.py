from selenium.webdriver.remote.webdriver import WebDriver
from pages import IFramePage


def test_iframe_initial_text(driver: WebDriver, base_url: str) -> None:
    page = IFramePage(driver, base_url=base_url).open()

    text = page.get_editor_text()

    assert "Your content goes here." in text


def test_iframe_text_can_be_updated(driver: WebDriver, base_url: str) -> None:
    page = IFramePage(driver, base_url=base_url).open()

    new_text = "Micah was here."
    page.set_editor_text(new_text)

    updated = page.get_editor_text()
    assert updated == new_text