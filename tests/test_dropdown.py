from pages import DropdownPage


def test_dropdown_default_selection(driver, base_url):
    page = DropdownPage(driver, base_url)
    page.open()

    assert page.selected_text() == "Please select an option"


def test_dropdown_can_select_option_1(driver, base_url):
    page = DropdownPage(driver, base_url)
    page.open()

    page.select_by_value("1")
    assert page.selected_text() == "Option 1"


def test_dropdown_can_select_option_2(driver, base_url):
    page = DropdownPage(driver, base_url)
    page.open()

    page.select_by_visible_text("Option 2")
    assert page.selected_text() == "Option 2"