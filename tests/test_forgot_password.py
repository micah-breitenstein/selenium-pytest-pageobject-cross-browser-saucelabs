import pytest
from pages import ForgotPasswordPage

def test_forgot_password_submit_shows_known_outcome(driver, base_url):
    """
    On the public heroku instance, submit may lead to an Internal Server Error.
    On some local clones/older deployments, it may show a success message.

    This test accepts either outcome so your suite stays stable.
    """
    page = ForgotPasswordPage(driver, base_url=base_url).open()
    result = page.retrieve_password("micah@example.com")

    assert result.is_internal_server_error() or result.is_success_message(), (
        "Unexpected forgot password result page.\n\n"
        f"Body text was:\n{result.body_text()}"
    )