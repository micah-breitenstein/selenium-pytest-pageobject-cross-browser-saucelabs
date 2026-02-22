import requests
from pages import BrokenImagesPage


def _is_img_broken(driver, img_element) -> bool:
    return driver.execute_script(
        "return arguments[0].complete && arguments[0].naturalWidth === 0;",
        img_element,
    )


def test_broken_images_api_status_codes(driver, base_url):
    page = BrokenImagesPage(driver, base_url)
    page.open()

    srcs = page.image_srcs()
    assert srcs, "No images found on the page"

    broken = []
    for url in srcs:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            broken.append((url, r.status_code))

    # Intentionally broken page: expect at least one broken image
    assert broken, "Expected at least one broken image, but all returned 200"
    print("Broken images (HTTP):", broken)


def test_broken_images_browser_detects_broken(driver, base_url):
    page = BrokenImagesPage(driver, base_url)
    page.open()

    imgs = driver.find_elements(*page.IMAGES)
    assert imgs, "No images found on the page"

    broken_count = sum(1 for img in imgs if _is_img_broken(driver, img))
    assert broken_count >= 1, "Expected at least one broken image via naturalWidth"
    print("Broken images (browser):", broken_count)
