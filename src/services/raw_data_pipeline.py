"""
src/services/raw_data_pipeline.py

This module orchestrates the complete raw data parsing pipeline for lalafo.kg,
starting from the main page, through categories, subcategories, raw ads, and product details.

Main Function:
- get_raw_data: The main asynchronous entry point that executes the entire parsing workflow,
  optionally uses cached data, and returns the complete raw data structure.

Author: Сh.Danil
Created: 2025-06-28
Last Modified: 2025-06-29
Version: 1.0.0
"""

from config import(
    REQUESTS_CLIENT, 
    SORT_METHOD
)
from parsers.category_parser import parse_categories_next_data_json
from services.ad_details_service import enrich_all_product_details_async
from services.raw_ads_service import fetch_all_raw_ads
from services.subcategory_service import(
    enrich_missing_subcategories_with_requests, 
    fetch_all_subcategories
)
from utils.json_utils import(
    load_existing_data, 
    save_data
)
from settings import LOGGER
from config import(
    URL, 
    BASE_URL
)
from config import(
    TEMP_DATA_PATH, 
    SHOULD_USE_TEMP_DATA
)
from typing import List
from data_types.raw_types import(
    RawBrand, 
    RawFormat
)


async def get_raw_data() -> RawFormat:
    """
    Executes the full raw data parsing pipeline asynchronously.

    Workflow:
    - Loads cached raw data from disk if enabled and available.
    - If no cached data, fetches main page HTML synchronously and parses categories.
    - Fetches subcategories asynchronously and enriches missing data using synchronous requests.
    - Fetches raw ads asynchronously for all categories and subcategories.
    - Optionally caches the parsed raw data to disk.
    - Enriches all product details asynchronously.
    - Returns the fully populated raw data dictionary.

    Returns:
        RawFormat: A dictionary containing all parsed brands, models, products, and details.
                   Returns an empty dict on failure.
    """
    LOGGER.info("Starting main parsing process")

    raw_data: RawFormat = {}

    if SHOULD_USE_TEMP_DATA:
        raw_data = load_existing_data(TEMP_DATA_PATH)

    try:
        if not raw_data:
            LOGGER.info("No temp data found, starting fresh parsing")
            LOGGER.info(f"Fetching main page HTML from {URL}")
            html: str = REQUESTS_CLIENT.get_html(URL)
            if html is None:
                LOGGER.error("Failed to fetch main page HTML")
                return {}

            LOGGER.info("Parsing categories from main page HTML")
            raw_data = parse_categories_next_data_json(html, BASE_URL + "/kyrgyzstan")

            LOGGER.info(f"Found {len(raw_data.get('brands', []))} categories")

            aiohttp_brands: List[RawBrand] = await fetch_all_subcategories(
                raw_data.get("brands", []), 
                BASE_URL + "/kyrgyzstan"
            )
            raw_data["brands"] = enrich_missing_subcategories_with_requests(
                aiohttp_brands, 
                BASE_URL + "/kyrgyzstan"
            )

            raw_data["brands"] = await fetch_all_raw_ads(
                raw_data, 
                additional_url=SORT_METHOD
            )

            if SHOULD_USE_TEMP_DATA:
                save_data(TEMP_DATA_PATH, raw_data)

        await enrich_all_product_details_async(raw_data)

        return raw_data

    except Exception as e:
        LOGGER.error(f"Error during parsing: {e}", exc_info=True)
        return {}
