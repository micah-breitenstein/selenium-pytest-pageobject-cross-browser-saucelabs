import pytest
from pages import ExitIntentPage

def test_exit_intent_modal_appears(driver, base_url):
    page = ExitIntentPage(driver, base_url=base_url).open()
    page.trigger_exit_intent()
    page.wait_for_modal(timeout=5)
    assert "MODAL" in page.modal_title().upper()