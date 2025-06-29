"""
src/utils/client_utils.py

This module provides utility functions for logging request counts made by 
the AiohttpClient and RequestsClient classes during a parsing session.

Main Function:
- log_client_request_counts: Logs how many requests were made by each HTTP client.

Author: Сh.Danil
Created: 2025-06-29
Last Modified: 2025-06-29
Version: 1.0.0
"""

from browser.aiohttp_client import AiohttpClient
from browser.requests_client import RequestsClient
from settings import LOGGER


def log_client_request_counts(aiohttp_client: AiohttpClient, requests_client: RequestsClient) -> None:
    """
    Logs the number of HTTP requests made by AiohttpClient and RequestsClient.

    Args:
        aiohttp_client (AiohttpClient): Instance of the asynchronous client.
        requests_client (RequestsClient): Instance of the synchronous client.

    Returns:
        None
    """
    LOGGER.info(f"AiohttpClient made {aiohttp_client.number_of_requests} requests")
    LOGGER.info(f"RequestsClient made {requests_client.number_of_requests} requests")
