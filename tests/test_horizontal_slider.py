from pages import HorizontalSliderPage


def test_horizontal_slider_can_set_value(driver, base_url):
    page = HorizontalSliderPage(driver, base_url).open()

    page.set_to(3.5)

    assert page.value_text() == "3.5"