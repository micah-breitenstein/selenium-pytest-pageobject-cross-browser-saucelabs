import pytest
from pages import EntryAdPage  # lazy-loaded via pages/__init__.py

@pytest.mark.no_safari
def test_entry_ad_modal_can_be_closed(driver, base_url):
    page = EntryAdPage(driver, base_url).open()

    # Fast probe so it doesn't burn action timeout
    if page.modal_is_visible(timeout=2):
        assert "MODAL" in page.modal_title().upper()
        page.close_modal()

        # Optional: quick confirm (DO NOT use action timeout here)
        assert page.modal_is_visible(timeout=0.2) is False

@pytest.mark.no_safari
def test_restart_ad_triggers_modal_again(driver, base_url):
    page = EntryAdPage(driver, base_url).open()

    # If it appears on initial open, close it (fast probe)
    if page.modal_is_visible(timeout=2):
        page.close_modal()

    page.restart_ad()

    # This is a case where we EXPECT it -> purposeful wait
    page.wait_for_modal(timeout=10)
    page.close_modal()