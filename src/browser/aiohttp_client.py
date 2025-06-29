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
from typing import Optional
from aiohttp import ClientSession, ClientTimeout
from settings import HEADERS, LOGGER


class AiohttpClient:
    def __init__(
        self,
        delay_between_requests: float = 0,
        retries: int = 1,
        timeout: float = 15
    ):
        """
        Initialize the AiohttpClient.

        Args:
            delay_between_requests (float): Delay in seconds between consecutive requests.
            retries (int): Number of retry attempts on failure.
            timeout (float): Timeout in seconds for each request.
        """
        self.delay_between_requests = delay_between_requests
        self.retries = retries
        self.timeout = ClientTimeout(total=timeout)
        self.number_of_requests = 0
        self._lock = asyncio.Lock()

    async def fetch_html(self, session: ClientSession, url: str) -> Optional[str]:
        """
        Asynchronously fetch HTML content from the specified URL with retry and delay.

        Args:
            session (ClientSession): An aiohttp ClientSession instance to make the request.
            url (str): The URL to fetch HTML content from.

        Returns:
            Optional[str]: The fetched HTML content as a string, or None if all attempts fail.
        """
        LOGGER.info("Fetching HTML via aiohttp: %s", url)
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
                        LOGGER.info("Delay between requests: %.2f seconds", self.delay_between_requests)
                        await asyncio.sleep(self.delay_between_requests)

                    LOGGER.info("Successfully fetched: %s", url)
                    return html
            except Exception as e:
                LOGGER.warning("Attempt %d to fetch %s failed: %s", attempt, url, e)
                if attempt == self.retries:
                    LOGGER.error("All retries failed for %s", url)
        return None