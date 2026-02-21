import pytest
from selenium.common.exceptions import NoAlertPresentException
from pages.context_menu_page import ContextMenuPage


def test_context_menu_alert_can_be_accepted(driver, base_url):
    page = ContextMenuPage(driver, base_url)
    page.open()

    page.context_click_hotspot()
    page.accept_alert()

    # after accepting, there should be no alert present
    with pytest.raises(NoAlertPresentException):
        _ = driver.switch_to.alert.text