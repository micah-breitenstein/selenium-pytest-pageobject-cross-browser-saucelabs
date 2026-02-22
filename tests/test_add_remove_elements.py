from pages import AddRemoveElementsPage


def test_add_one_delete_button(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element()
    page.wait_for_delete_count(1)
    assert page.delete_count() == 1


def test_add_thirty_then_delete_one(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element(times=30)
    page.wait_for_delete_count(30)
    assert page.delete_count() == 30

    page.click_delete_at_index(0)
    page.wait_for_delete_count(29)
    assert page.delete_count() == 29


def test_add_two_then_delete_all(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element(times=2)
    page.wait_for_delete_count(2)

    while page.delete_count() > 0:
        page.click_delete_at_index(0)

    page.wait_for_delete_count(0)
    assert page.delete_count() == 0
