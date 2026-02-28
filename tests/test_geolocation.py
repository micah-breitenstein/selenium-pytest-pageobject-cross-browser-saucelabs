# tests/test_geolocation.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


GEO_URL = "https://the-internet.herokuapp.com/geolocation"


def test_geolocation_shows_mocked_coords(driver):
    # pick something recognizable
    latitude = 37.7749
    longitude = -122.4194

    # 1) Grant permission for this origin (prevents prompt from blocking)
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {"origin": "https://the-internet.herokuapp.com", "permissions": ["geolocation"]},
    )

    # 2) Override location
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {"latitude": latitude, "longitude": longitude, "accuracy": 10},
    )

    # 3) Load page + click button
    driver.get(GEO_URL)
    driver.find_element(By.CSS_SELECTOR, "#content button").click()

    # 4) Assert values populate
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.find_element(By.ID, "lat-value").text.strip() != "")
    wait.until(lambda d: d.find_element(By.ID, "long-value").text.strip() != "")

    lat_text = driver.find_element(By.ID, "lat-value").text.strip()
    long_text = driver.find_element(By.ID, "long-value").text.strip()

    assert str(latitude) in lat_text
    assert str(longitude) in long_text