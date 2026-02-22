import time
from pages import DragAndDropPage

def test_drag_and_drop_swaps_twice(driver, base_url):
    page = DragAndDropPage(driver, base_url)
    page.open()

    before = page.header_texts()
    assert before == ("A", "B")
    time.sleep(1)  # the drag-and-drop demo is very slow to update, so we wait a bit before checking results

    page.swap_columns_html5()
    assert page.header_texts() == ("B", "A")
    time.sleep(1)  # wait a bit before checking results

    page.swap_columns_html5()
    assert page.header_texts() == ("A", "B")
    time.sleep(1)  # wait a bit before checking results