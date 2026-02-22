# conftest.py
import os
import time
import pytest
import logging

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSessionIdException,
    WebDriverException,
    NoSuchWindowException,
)
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
# BASE URL (single source of truth)
# -------------------------
@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url").rstrip("/")


# -------------------------
# SAUCE HELPERS
# -------------------------
def _sauce_hub(region: str) -> str:
    return f"https://ondemand.{region}.saucelabs.com/wd/hub"


def _make_remote_options(browser: str):
    if browser == "chrome":
        return webdriver.ChromeOptions()
    if browser == "firefox":
        return webdriver.FirefoxOptions()
    if browser == "edge":
        return webdriver.EdgeOptions()
    raise ValueError("For Sauce runs, use --browser=chrome|firefox|edge")


def _create_remote(request):
    browser = request.config.getoption("--browser")

    sauce_user = os.getenv("SAUCE_USERNAME")
    sauce_key = os.getenv("SAUCE_ACCESS_KEY")
    if not sauce_user or not sauce_key:
        raise RuntimeError("Set SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables")

    platform = request.config.getoption("--platform")
    browser_version = request.config.getoption("--browser-version")
    region = request.config.getoption("--sauce-region")

    options = _make_remote_options(browser)

    browser_name = "MicrosoftEdge" if browser == "edge" else browser
    options.set_capability("browserName", browser_name)
    options.set_capability("platformName", platform)

    if not (browser == "edge" and str(browser_version).startswith("latest")):
        options.set_capability("browserVersion", browser_version)

    sauce_opts = {
        "username": sauce_user,
        "accessKey": sauce_key,
        "name": request.module.__name__,
        "build": os.getenv("BUILD_TAG", "selenium-python-basics"),
    }
    options.set_capability("sauce:options", sauce_opts)

    return webdriver.Remote(
        command_executor=_sauce_hub(region),
        options=options,
    )


# -------------------------
# CHROMEDRIVER SERVICE (WDM only once per run)
# -------------------------
@pytest.fixture(scope="session")
def chrome_service():
    return ChromeService(ChromeDriverManager().install())


def _create_local_chrome(request, chrome_service):
    headless = request.config.getoption("--headless")
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")
    return webdriver.Chrome(service=chrome_service, options=options)


def _create_local_safari_with_retry(base_url: str, attempts: int = 3, delay_s: float = 0.6):
    """
    SafariDriver can sometimes hand out a session id but immediately invalidate it.
    We validate by issuing a trivial command right away. If it fails, retry.
    """
    last_exc: Exception | None = None
    for i in range(1, attempts + 1):
        drv = None
        try:
            drv = webdriver.Safari()
            # "Health check": first command must succeed or this session is toast.
            drv.get(base_url + "/")
            return drv
        except (InvalidSessionIdException, WebDriverException) as e:
            last_exc = e
            try:
                if drv:
                    drv.quit()
            except Exception:
                pass
            time.sleep(delay_s)
    raise RuntimeError(
        "SafariDriver session becomes invalid immediately (InvalidSessionIdException).\n"
        "Most common causes:\n"
        "  - Safari remote automation not enabled/authorized\n"
        "  - xdist (-n) enabled (Safari can't run under multiple workers)\n"
        f"Last error: {type(last_exc).__name__}: {last_exc}"
    )


def _xdist_num_workers(config) -> int:
    # pytest-xdist sets config.option.numprocesses (int or 'auto').
    n = getattr(getattr(config, "option", None), "numprocesses", 0)
    if n == "auto":
        return 999  # treat as enabled
    try:
        return int(n)
    except Exception:
        return 0


# -------------------------
# DRIVER FIXTURE
# - Chrome local: module-scoped (fast)
# - Safari local: function-scoped (new browser per test, stable model)
# - Remote: module-scoped (fast)
# -------------------------
@pytest.fixture(scope="module")
def _module_driver_chrome(request, chrome_service):
    drv = _create_local_chrome(request, chrome_service)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture(scope="module")
def _module_driver_remote(request):
    drv = _create_remote(request)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def driver(request, base_url):
    browser = request.config.getoption("--browser")
    remote = request.config.getoption("--remote")

    if remote:
        return request.getfixturevalue("_module_driver_remote")

    # HARD BLOCK: local Safari + xdist => not supported
    if browser == "safari":
        workers = _xdist_num_workers(request.config)
        if workers and workers > 0:
            raise RuntimeError(
                "You are running with pytest-xdist (-n enabled). Local Safari cannot run under xdist.\n"
                "Run Safari serially:\n"
                "  python -m pytest -q -s --browser=safari -n 0 --base-url=http://127.0.0.1:9292\n"
                "Or use Chrome for parallel:\n"
                "  python -m pytest -q -s --browser=chrome -n auto --base-url=http://127.0.0.1:9292"
            )

        drv = _create_local_safari_with_retry(base_url=base_url)
        try:
            yield drv
        finally:
            try:
                drv.quit()
            except Exception:
                pass
        return

    if browser == "chrome":
        drv = request.getfixturevalue("_module_driver_chrome")
        yield drv
        return

    raise ValueError("Local runs support --browser=chrome or --browser=safari (remote supports chrome|firefox|edge)")


# -------------------------
# OPTIONAL: Reset state between tests
# -------------------------
@pytest.fixture(autouse=True)
def _reset_between_tests(driver, base_url, request):
    browser = request.config.getoption("--browser")
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

        # Safari can be touchy about about:blank; take it home instead.
        if browser == "safari":
            driver.get(base_url + "/")
        else:
            driver.get("about:blank")

    except (InvalidSessionIdException, NoSuchWindowException, WebDriverException):
        pass
    except Exception:
        pass


# -------------------------
# PAGE OBJECT FACTORY
# -------------------------
@pytest.fixture
def page(driver, base_url):
    def _make(PageClass, *args, **kwargs):
        return PageClass(driver, base_url=base_url, *args, **kwargs)
    return _make


@pytest.fixture
def landing(driver, base_url):
    from pages.landing_page import LandingPage
    return LandingPage(driver, base_url=base_url)


# -------------------------
# SCREENSHOT + SAUCE PASS/FAIL ON REPORT
# -------------------------
def _safe_screenshot(drv, path: str) -> tuple[bool, str | None]:
    """
    SafariDriver screenshots can hang for a long time.
    We skip screenshots entirely on Safari to avoid 20+ minute runs on failures.
    """
    try:
        browser_name = drv.capabilities.get("browserName", "").lower()
        if browser_name == "safari":
            return (False, "Skipped screenshot on Safari (can hang)")

        ok = drv.save_screenshot(path)
        return (bool(ok), None)
    except (InvalidSessionIdException, NoSuchWindowException, WebDriverException) as e:
        return (False, f"{type(e).__name__}: {e}")
    except Exception as e:
        return (False, f"{type(e).__name__}: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    drv = item.funcargs.get("driver", None)
    if not drv:
        return

    if report.when == "call" and report.failed:
        os.makedirs("artifacts", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = f"artifacts/{item.name}-{ts}.png"

        ok, err = _safe_screenshot(drv, path)
        if ok:
            report.longrepr = f"{report.longrepr}\n\nScreenshot saved: {path}"
        else:
            report.longrepr = f"{report.longrepr}\n\nScreenshot skipped: {err}"

    if item.config.getoption("--remote") and report.when == "call":
        result = "passed" if report.passed else "failed"
        try:
            drv.execute_script(f"sauce:job-result={result}")
        except Exception:
            pass


# -------------------------
# MARKERS / SAFARI SKIPS / LOGGING CONFIG
# -------------------------
def pytest_configure(config):
    os.environ["BASE_URL"] = config.getoption("--base-url")

    # Register markers (prevents "unknown marker" warnings)
    config.addinivalue_line(
        "markers",
        "no_safari: skip this test when running with Safari WebDriver",
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def pytest_runtest_setup(item):
    """
    If a test is marked with @pytest.mark.no_safari, skip it when --browser=safari.
    """
    browser = item.config.getoption("--browser", default="safari").lower()
    if browser == "safari" and item.get_closest_marker("no_safari"):
        pytest.skip("Skipped on Safari (SafariDriver limitation).")