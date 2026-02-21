from pages.dynamic_content_page import DynamicContentPage


def test_dynamic_content_has_rows(driver, base_url):
    page = DynamicContentPage(driver, base_url=base_url)
    page.open_page()

    # This site can change; assert "at least 3" dynamic content blocks
    assert page.row_count() >= 3, f"Expected at least 3 rows, got {page.row_count()}"

    texts = page.rows_text()
    assert all(t.strip() for t in texts), f"Expected non-empty text in all rows, got: {texts}"


def test_dynamic_content_changes_after_refresh(driver, base_url):
    page = DynamicContentPage(driver, base_url=base_url)
    page.open_page()

    before = page.rows_text()

    changed = False
    for _ in range(5):
        page.refresh()
        after = page.rows_text()
        if after != before:
            changed = True
            break

    assert changed