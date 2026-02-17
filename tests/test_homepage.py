from pages.homepage import HomePage


def test_homepage_heading_safari(driver):
    homepage = HomePage(driver)

    homepage.load()

    assert homepage.get_heading_text() == "Example Domain"
