from pages.challenging_dom_page import ChallengingDomPage


def test_delete_first_row_by_column_text(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    page.click_delete_by_column_text(0, "Iuvaret0")

    assert page.current_url().endswith("#delete"), f"Unexpected URL: {page.current_url()}"


def test_delete_first_row_dynamic(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    first_row = page.rows()[0]
    first_cell_text = first_row.find_elements("tag name", "td")[0].text.strip()

    page.click_delete_by_column_text(0, first_cell_text)

    assert page.current_url().endswith("#delete")


def test_challenging_dom_has_three_buttons(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    texts = page.button_texts()
    assert set(texts.keys()) == {"blue", "red", "green"}
    assert all(texts[c] for c in texts), f"Expected all button texts to be non-empty, got: {texts}"


def test_button_labels_change_when_clicked(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    before = page.button_texts()
    page.click_button("blue")
    after = page.wait_for_button_texts_to_change(before)

    changed = {k for k in before if before[k] != after[k]}
    assert changed, f"Expected at least one button label to change. Before={before}, After={after}"


def test_canvas_changes_when_button_clicked(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    before = page.canvas_data_url()
    page.click_button("blue")
    after = page.wait_for_canvas_change(before)   # <-- wait, don't read immediately

    assert before != after, "Expected canvas image to change after button click"


def test_answer_changes_when_button_clicked(driver, base_url):
    page = ChallengingDomPage(driver, base_url)
    page.open()

    before = page.answer_value()                  # <-- should be canvas-derived
    page.click_button("green")
    after = page.wait_for_answer_to_change(before)

    assert before != after, f"Expected Answer to change. Before={before}, After={after}"