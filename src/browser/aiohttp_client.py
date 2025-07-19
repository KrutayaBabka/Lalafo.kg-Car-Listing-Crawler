"""
src/browser/aiohttp_client.py

This module defines an asynchronous HTTP client using aiohttp for fetching HTML content
with configurable retry logic, timeout, and optional delay between requests.

Class:
- AiohttpClient: Encapsulates HTTP GET request functionality with logging and error handling.

Dependencies:
- aiohttp: for asynchronous HTTP client requests.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.0
"""

import asyncio
import random
from typing import Optional
from aiohttp import ClientSession, ClientTimeout
from settings import HEADERS, LOGGER


class AiohttpClient:
    def __init__(
        self,
        delay_between_requests: float = 0,
        retries: int = 10,
        timeout: float = 15,
        max_concurrent_requests: int = 30,
    ):
        """
        Initialize the AiohttpClient.

        Args:
            delay_between_requests (float): Base delay (in seconds) between requests.
            retries (int): Number of retry attempts on failure.
            timeout (float): Timeout (in seconds) per request.
            max_concurrent_requests (int): Max number of concurrent requests.
        """
        self.delay_between_requests = delay_between_requests
        self.retries = retries
        self.timeout = ClientTimeout(total=timeout)
        self.number_of_requests = 0
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def fetch_html(self, session: ClientSession, url: str) -> Optional[str]:
        """
        Fetch HTML content from the given URL with retries, delay, and semaphore control.

        Args:
            session (ClientSession): aiohttp session object.
            url (str): URL to fetch.

        Returns:
            Optional[str]: HTML content or None if all retries fail.
        """
        LOGGER.info("Fetching HTML via aiohttp: %s", url)

        async with self._semaphore:
            for attempt in range(1, self.retries + 1):
                try:
                    async with session.get(url, headers=HEADERS, timeout=self.timeout) as response:
                        response.raise_for_status()
                        html = await response.text()

                        if not html.strip():
                            LOGGER.warning("Fetched HTML is empty for %s", url)
                            return None

                        async with self._lock:
                            self.number_of_requests += 1

                        if self.delay_between_requests > 0:
                            delay = random.uniform(
                                self.delay_between_requests,
                                self.delay_between_requests + 0.5
                            )
                            LOGGER.info("Random delay: %.2f seconds", delay)
                            await asyncio.sleep(delay)

                        LOGGER.info("Successfully fetched: %s", url)
                        return html

                except Exception as e:
                    if self.delay_between_requests > 0:
                        delay = random.uniform(
                            self.delay_between_requests,
                            self.delay_between_requests + 0.5
                        )
                        LOGGER.info("Retry delay: %.2f seconds", delay)
                        await asyncio.sleep(delay)

                    LOGGER.warning("Attempt %d to fetch %s failed: %s", attempt, url, e)

                    if attempt == self.retries:
                        LOGGER.error("All retries failed for %s", url)

        return None