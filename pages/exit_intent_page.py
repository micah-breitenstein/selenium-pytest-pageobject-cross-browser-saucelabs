# pages/exit_intent_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class ExitIntentPage(BasePage):
    PATH = "/exit_intent"

    MODAL = (By.CSS_SELECTOR, ".modal")
    MODAL_TITLE = (By.CSS_SELECTOR, ".modal-title h3")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-footer p")  # "Close" text

    def open(self):
        self.driver.get(self.config.base_url + self.PATH)
        # Avoid racing the JS that registers the exit-intent listeners
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return self

    def trigger_exit_intent(self):
        # Safari-hardened synthetic exit intent trigger
        self.driver.execute_script(
            """
            (function() {
              const el = document.documentElement;

              const evt = new MouseEvent('mouseout', {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: 0,
                clientY: 0,
                relatedTarget: null
              });

              try { Object.defineProperty(evt, 'toElement', { get: () => null }); } catch(e) {}
              try { Object.defineProperty(evt, 'relatedTarget', { get: () => null }); } catch(e) {}

              el.dispatchEvent(evt);

              const evt2 = new MouseEvent('mouseleave', {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: 0,
                clientY: 0,
                relatedTarget: null
              });

              try { Object.defineProperty(evt2, 'toElement', { get: () => null }); } catch(e) {}
              try { Object.defineProperty(evt2, 'relatedTarget', { get: () => null }); } catch(e) {}

              el.dispatchEvent(evt2);
            })();
            """
        )
        return self

    def wait_for_modal(self, timeout: int = 5):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.MODAL)
        )

    def modal_is_visible(self, timeout: int = 2) -> bool:
        try:
            self.wait_for_modal(timeout=timeout)
            return True
        except Exception:
            return False

    def modal_title(self, timeout: int = 5) -> str:
        el = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.MODAL_TITLE)
        )
        return el.text

    def close_modal(self, timeout: int = 5):
        # The "Close" control is a <p> element in the footer on this site.
        btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.MODAL_CLOSE)
        )
        btn.click()

        # Wait until modal is gone/hidden
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self.MODAL)
        )
        return self