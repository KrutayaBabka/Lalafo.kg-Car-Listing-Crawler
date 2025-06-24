import asyncio
import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import logger


class SeleniumClient:
    def __init__(self, headless: bool = True, wait_time: float = 1.5, restart_every_n_requests: int = 10):
        self.headless = headless
        self.wait_time = wait_time
        self.restart_every_n_requests = restart_every_n_requests
        self._requests_made = 0
        self._initialize_driver()

    def _initialize_driver(self):
        options: Options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-unsafe-swiftshader")
        options.page_load_strategy = 'eager'

        logger.info("Initializing Chrome WebDriver (headless=%s)", self.headless)
        self.driver: WebDriver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        logger.info("Chrome WebDriver initialized")

    def _maybe_restart_driver(self):
        self._requests_made += 1
        if self._requests_made >= self.restart_every_n_requests:
            logger.info("Restart threshold reached (%d). Restarting WebDriver.", self._requests_made)
            self.close()
            self._initialize_driver()
            self._requests_made = 0

    def get_html(self, url: str, wait_for_selector: str | None = None, retries: int = 3) -> str:
        self._maybe_restart_driver()

        logger.info("Navigating to URL: %s", url)
        for attempt in range(1, retries + 1):
            try:
                self.driver.get(url)

                if wait_for_selector:
                    logger.info("Waiting for element: %s", wait_for_selector)
                    WebDriverWait(self.driver, timeout=10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
                    )
                    logger.info("Element %s found", wait_for_selector)

                html = self.driver.page_source
                logger.info("Page source retrieved successfully from URL: %s", url)
                return html

            except Exception as e:
                logger.warning("Attempt %d to load %s failed: %s", attempt, url, e)
                if attempt == retries:
                    logger.error("All retries failed for %s", url)
                    raise
                time.sleep(2)

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            logger.warning("Error while closing WebDriver: %s", e)
        logger.info("Chrome WebDriver closed")
    