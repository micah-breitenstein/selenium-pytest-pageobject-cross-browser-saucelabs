import requests
import pytest
from requests.auth import HTTPBasicAuth
from pages import BasicAuthPage

@pytest.mark.no_safari
def test_basic_auth_success(driver, base_url):
    page = BasicAuthPage(driver, base_url)
    page.open_with_credentials("admin", "admin")
    assert "Congratulations" in page.get_message()

def test_basic_auth_failure_returns_401(base_url):
    url = f"{base_url.rstrip('/')}/basic_auth"
    resp = requests.get(url, auth=HTTPBasicAuth("wrong", "wrong"))
    assert resp.status_code == 401
