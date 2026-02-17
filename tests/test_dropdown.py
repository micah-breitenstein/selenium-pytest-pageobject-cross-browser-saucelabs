from pages.landing_page import LandingPage

def test_dropdown_select(landing):
    page = landing.load().go_to_dropdown()
    page.select_by_visible_text("Option 2")
    assert page.selected_text() == "Option 2"