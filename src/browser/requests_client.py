"""
src/browser/requests_client.py

This module provides a simple HTTP client wrapper around the 'requests' library,
allowing configurable retries, timeouts, and delay between requests.

Class:
- RequestsClient: A client to fetch HTML content via HTTP GET with logging, retries, and throttling.

Dependencies:
- requests: for synchronous HTTP requests.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.0
"""

import time
from typing import Optional
import requests
from requests import Response
from settings import HEADERS, LOGGER


class RequestsClient:
    """
    HTTP client for fetching HTML content with retry logic and optional delay between requests.

    Attributes:
        delay_between_requests (float): Seconds to wait between requests to avoid rate limiting.
        timeout (float): Request timeout in seconds.
        retries (int): Number of retry attempts on failure.
        number_of_requests (int): Counter of successful requests made.
    """

    def __init__(self, delay_between_requests: float = 0, timeout: float = 10, retries: int = 1):
        self.delay_between_requests = delay_between_requests
        self.timeout = timeout
        self.retries = retries
        self.number_of_requests = 0

    def get_html(self, url: str) -> Optional[str]:
        """
        Fetch the HTML content of a given URL using HTTP GET with retries and delay.

        Args:
            url (str): The URL to fetch.

        Returns:
            Optional[str]: The HTML content as a string if successful, None otherwise.
        """
        LOGGER.info("Fetching HTML via requests: %s", url)
        for attempt in range(1, self.retries + 1):
            try:
                response: Response = requests.get(url, headers=HEADERS, timeout=self.timeout)
                response.raise_for_status()
                self.number_of_requests += 1

                if self.delay_between_requests > 0:
                    LOGGER.info("Delay between requests: %.2f seconds", self.delay_between_requests)
                    time.sleep(self.delay_between_requests)

                LOGGER.info("Successfully fetched: %s", url)
                return response.text

            except Exception as e:
                LOGGER.warning("Attempt %d to fetch %s failed: %s", attempt, url, e)
                if attempt == self.retries:
                    LOGGER.error("All retries failed for %s", url)
        return None
