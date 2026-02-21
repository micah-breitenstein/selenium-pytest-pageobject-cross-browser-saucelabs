from pages.disappearing_elements_page import DisappearingElementsPage


def test_core_menu_items_are_present(driver, base_url):
    page = DisappearingElementsPage(driver, base_url)
    page.open()

    texts = page.menu_texts()

    for required in ["Home", "About", "Contact Us", "Portfolio"]:
        assert required in texts, f"Expected '{required}' in menu, got {texts}"


def test_gallery_menu_item_is_optional(driver, base_url):
    page = DisappearingElementsPage(driver, base_url)
    page.open()

    # This should never fail: Gallery may or may not exist on a given load
    _ = page.has_menu_item("Gallery")

def test_gallery_eventually_appears_demo(driver, base_url):
    page = DisappearingElementsPage(driver, base_url)
    page.open()

    for _ in range(10):
        if page.has_menu_item("Gallery"):
            return
        page.refresh()

    assert False, "Gallery did not appear after 10 refreshes (random behavior)"