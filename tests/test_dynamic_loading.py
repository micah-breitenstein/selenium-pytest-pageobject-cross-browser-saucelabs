from pages.landing_page import LandingPage


def test_dynamic_loading_example_2(landing):
    page = (
        landing
        .load()
        .go_to_dynamic_loading()
        .open_example_2()
        .start_loading()
    )

    assert "Hello World!" in page.finish_text()