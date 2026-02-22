from pages import AddRemoveElementsPage


def test_add_one_delete_button(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element()
    page.wait_for_delete_count(1)
    assert page.delete_count() == 1


def test_add_three_hundred_then_delete_one(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element(times=300)
    page.wait_for_delete_count(300)
    assert page.delete_count() == 300

    page.click_delete_at_index(0)
    page.wait_for_delete_count(299)
    assert page.delete_count() == 299


def test_add_two_then_delete_all(driver, base_url):
    page = AddRemoveElementsPage(driver, base_url)
    page.open()

    page.add_element(times=2)
    page.wait_for_delete_count(2)

    while page.delete_count() > 0:
        page.click_delete_at_index(0)

    page.wait_for_delete_count(0)
    assert page.delete_count() == 0
