import os
import pytest
import logging

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# -------------------------
# CLI OPTIONS
# -------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="safari",
        help="Browser to run tests against: safari, chrome, firefox, edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (local Chrome only)",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://the-internet.herokuapp.com",
        help="Base URL for the app under test",
    )
    parser.addoption(
        "--remote",
        action="store_true",
        help="Run tests on Sauce Labs",
    )
    parser.addoption(
        "--platform",
        action="store",
        default="macOS 13",
        help='Sauce platformName (e.g. "macOS 13", "Windows 11", "Windows 10")',
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="latest",
        help='Sauce browserVersion (e.g. "latest", "latest-1", "120")',
    )
    parser.addoption(
        "--sauce-region",
        action="store",
        default="us-west-1",
        help="Sauce region: us-west-1, us-east-1, eu-central-1",
    )


# -------------------------
# BASE URL FIXTURE
# -------------------------
@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


def _sauce_hub(region: str) -> str:
    return f"https://ondemand.{region}.saucelabs.com/wd/hub"


def _make_remote_options(browser: str):
    """
    Returns the correct Selenium Options object for the given browser.
    """
    if browser == "chrome":
        return webdriver.ChromeOptions()
    if browser == "firefox":
        return webdriver.FirefoxOptions()
    if browser == "edge":
        return webdriver.EdgeOptions()
    raise ValueError("For Sauce runs, use --browser=chrome|firefox|edge")


# -------------------------
# DRIVER FIXTURE
# -------------------------
@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://127.0.0.1:9292").rstrip("/")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")

    if remote:
        sauce_user = os.getenv("SAUCE_USERNAME")
        sauce_key = os.getenv("SAUCE_ACCESS_KEY")
        if not sauce_user or not sauce_key:
            raise RuntimeError("Set SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables")

        platform = request.config.getoption("--platform")
        browser_version = request.config.getoption("--browser-version")
        region = request.config.getoption("--sauce-region")

        options = _make_remote_options(browser)

        # Sauce is picky about Edge naming
        browser_name = "MicrosoftEdge" if browser == "edge" else browser
        options.set_capability("browserName", browser_name)

        # platformName is required
        options.set_capability("platformName", platform)

        # Sauce commonly accepts "latest" for Chrome/Firefox.
        # Edge sometimes rejects "latest" depending on region/availability.
        if not (browser == "edge" and str(browser_version).startswith("latest")):
            options.set_capability("browserVersion", browser_version)

        sauce_opts = {
            "username": sauce_user,
            "accessKey": sauce_key,
            "name": request.node.name,
            "build": os.getenv("BUILD_TAG", "selenium-python-basics"),
        }
        options.set_capability("sauce:options", sauce_opts)

        driver = webdriver.Remote(
            command_executor=_sauce_hub(region),
            options=options,
        )

    else:
        # Local run
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            else:
                options.add_argument("--start-maximized")

            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )

        elif browser == "safari":
            driver = webdriver.Safari()

        else:
            raise ValueError("Local runs support --browser=chrome or --browser=safari")

    yield driver
    driver.quit()


# -------------------------
# PAGE OBJECT FACTORY
# -------------------------
@pytest.fixture
def page(driver, base_url):
    def _make(PageClass, *args, **kwargs):
        return PageClass(driver, base_url=base_url, *args, **kwargs)
    return _make


# -------------------------
# LANDING PAGE FIXTURE
# -------------------------
@pytest.fixture
def landing(driver, base_url):
    from pages.landing_page import LandingPage
    return LandingPage(driver, base_url=base_url)


# -------------------------
# SCREENSHOT + SAUCE PASS/FAIL ON REPORT
# -------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    drv = item.funcargs.get("driver", None)
    if not drv:
        return

    # Screenshot on failure
    if report.when == "call" and report.failed:
        os.makedirs("artifacts", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = f"artifacts/{item.name}-{ts}.png"
        drv.save_screenshot(path)
        report.longrepr = f"{report.longrepr}\n\nScreenshot saved: {path}"

    # Tell Sauce pass/fail
    if item.config.getoption("--remote") and report.when == "call":
        result = "passed" if report.passed else "failed"
        try:
            drv.execute_script(f"sauce:job-result={result}")
        except Exception:
            # Don't fail the test run if Sauce reporting fails
            pass


# -------------------------
# LOGGING CONFIG
# -------------------------
def pytest_configure(config):
    os.environ["BASE_URL"] = config.getoption("--base-url")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
