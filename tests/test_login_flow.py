from pages import LandingPage


def test_login_success(landing):
    secure = (
        landing
        .load()
        .go_to_login()
        .login("tomsmith", "SuperSecretPassword!")
    )

    assert "Secure Area" in secure.header()
    assert "You logged into a secure area" in secure.flash_message()


def test_login_failure_shows_error(landing):
    login = (
        landing
        .load()
        .go_to_login()
    )

    login.login_expect_failure("baduser", "badpass")
    assert "Your username is invalid" in login.flash_message()
