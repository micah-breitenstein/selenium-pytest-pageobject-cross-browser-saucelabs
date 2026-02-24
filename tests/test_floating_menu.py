import pytest
from pages import FloatingMenuPage


@pytest.mark.parametrize("menu_item, expected_hash", [
    ("Home", "#home"),
    ("News", "#news"),
    ("Contact", "#contact"),
    ("About", "#about"),
])
def test_floating_menu_stays_visible_and_updates_hash(driver, base_url, menu_item, expected_hash):
    page = FloatingMenuPage(driver, base_url=base_url).open()

    assert page.menu_is_displayed(), "Menu should be visible on load"

    page.scroll_by(1200)
    assert page.menu_is_displayed(), "Menu should remain visible after scroll"

    page.click_menu_item(menu_item)

    # Hash updates should be instant, but give Safari a beat if needed
    assert page.current_hash().lower() == expected_hash