from selenium.webdriver.remote.webdriver import WebDriver

class DigestAuthPage:
    URL_PATH = "/digest_auth"
    # credentials baked into the URL
    AUTH_URL_TEMPLATE = "https://{user}:{pw}@the-internet.herokuapp.com{path}"

    def __init__(self, driver: WebDriver, base_url: str, user="admin", pw="admin"):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.user = user
        self.pw = pw

    def open(self):
        auth_url = self.AUTH_URL_TEMPLATE.format(
            user=self.user,
            pw=self.pw,
            path=self.URL_PATH
        )
        self.driver.get(auth_url)

    def current_url(self) -> str:
        return self.driver.current_url