"""
src/services/subcategory_service.py

This module handles the enrichment of category data with subcategory (model) information
by parsing subcategories from web pages.

Key features:
- Asynchronous fetching and parsing of subcategories using aiohttp.
- Fallback synchronous retry with requests for categories that failed in async mode.
- Integrated tqdm progress bars for improved tracking of async and sync subcategory enrichment.

Dependencies:
- aiohttp: for asynchronous HTTP requests
- requests: used internally via REQUESTS_CLIENT fallback
- tqdm: for CLI progress bars

Functions:
- fetch_and_parse_subcategories: Asynchronously fetches and parses subcategories for a single brand.
- fetch_all_subcategories: Concurrently fetches subcategories for all brands.
- enrich_missing_subcategories_with_requests: Retries subcategory fetching synchronously for failed brands.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-28
Version: 1.0.0
"""


import asyncio
from typing import Any, Coroutine, List
from aiohttp import ClientSession
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from data_types.raw_types import RawBrand, RawModel
from settings import LOGGER
from config import(
    AIOHTTP_CLIENT, 
    REQUESTS_CLIENT
)
from parsers.subcategory_parser import parse_subcategories_next_data_json


async def fetch_and_parse_subcategories(
    session: ClientSession, 
    category: RawBrand, 
    base_url: str
) -> RawBrand:
    """
    Asynchronously fetch and parse subcategories (models) for a single brand.

    Args:
        session (ClientSession): An active aiohttp session.
        category (RawBrand): Dictionary containing brand metadata, including a 'url'.
        base_url (str): Base URL context for parsing.

    Returns:
        RawBrand: Updated brand dictionary with a "models" field (list of subcategories).
    """
    try:
        LOGGER.info(f"Fetching subcategories for '{category['name']}' from {category['url']}")
        html: str = await AIOHTTP_CLIENT.fetch_html(session, category["url"])
        if html is None:
            LOGGER.warning(f"Failed to fetch HTML for {category['name']}, returning empty subcategories")
            return {
                **category,
                "models": []
            }

        result: RawBrand = parse_subcategories_next_data_json(html, base_url)
        subcategories: List[RawModel] = result.get("models", [])

        LOGGER.info(f"Found {len(subcategories)} subcategories for '{category['name']}'")

        return {
            **category,
            "models": subcategories
        }

    except Exception as e:
        LOGGER.error(f"Failed to fetch subcategories for {category['name']}: {e}", exc_info=True)

        return {
            **category,
            "models": []
        }


async def fetch_all_subcategories(
    brands: List[RawBrand],
    base_url: str
) -> List[RawBrand]:
    async with ClientSession() as session:
        tasks = [
            fetch_and_parse_subcategories(session, category, base_url)
            for category in brands
        ]
        # Здесь результаты будут именно в порядке brands[0], brands[1], ...
        updated_brands = await asyncio.gather(*tasks)
        LOGGER.info(f"Fetched {len(updated_brands)} categories with subcategories")
        return updated_brands
    

def enrich_missing_subcategories_with_requests(
    brands: List[RawBrand],
    base_url: str,
) -> List[RawBrand]:
    """
    Retry parsing subcategories synchronously using requests for brands
    that failed to populate subcategories during async enrichment.

    Args:
        brands (List[RawBrand]): List of brand dictionaries to retry.
        base_url (str): Base URL context for parsing.

    Returns:
        List[RawBrand]: Updated list with missing subcategories filled where possible.
    """
    for brand in tqdm(brands, desc="Retrying missing subcategories (requests)"):
        models: List[RawModel] = brand.get("models", [])
        if not models:
            LOGGER.info(f"Retrying with RequestsClient for '{brand.get('name', 'Unknown')}' with no subcategories")

            try:
                html: str = REQUESTS_CLIENT.get_html(brand["url"])
                if html is None:
                    LOGGER.warning(f"Failed to fetch HTML via RequestsClient for '{brand.get('name', 'Unknown')}', skipping")
                    continue

                result: RawBrand = parse_subcategories_next_data_json(html, base_url)
                brand["models"] = result.get("models", [])
                LOGGER.info(
                    f"Parsed {len(brand['models'])} subcategories for '{brand.get("name", "Unknown")}' using RequestsClient"
                )
            except Exception as e:
                LOGGER.error(f"Error processing '{brand.get("name", "Unknown")}' with RequestsClient: {e}", exc_info=True)
                brand["models"] = []

    return brands

