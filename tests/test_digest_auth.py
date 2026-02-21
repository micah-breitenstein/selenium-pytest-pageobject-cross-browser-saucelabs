from pages.digest_auth_page import DigestAuthPage

def test_digest_auth_succeeds(driver, base_url):
    page = DigestAuthPage(driver, base_url)
    page.open()

    # digest auth succeeds and you end up on the protected page
    assert "digest_auth" in page.current_url()