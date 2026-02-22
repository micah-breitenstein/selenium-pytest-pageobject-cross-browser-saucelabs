from pages import LandingPage

def test_checkboxes_toggle(landing):
    page = landing.load().go_to_checkboxes()

    assert page.is_checked(page.CB1) is False
    assert page.is_checked(page.CB2) is True

    page.set_checked(page.CB1, True)
    page.set_checked(page.CB2, False)

    assert page.is_checked(page.CB1) is True
    assert page.is_checked(page.CB2) is False
