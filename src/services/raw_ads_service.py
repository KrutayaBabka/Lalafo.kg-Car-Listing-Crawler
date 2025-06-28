"""
raw_ads_service.py

Asynchronous service module for fetching raw advertisement links data
from paginated sources concurrently using aiohttp.

This module provides functions to:
- Fetch paginated raw ads HTML content asynchronously.
- Parse and aggregate product links from multiple pages.
- Traverse brands and models structure, fetching raw ads for each.
- Display multi-level progress bars for brands, models, and pages
  with tqdm, ensuring a clear and smooth CLI user experience.

Dependencies:
- aiohttp for asynchronous HTTP requests.
- tqdm for progress bars.

Usage example:
    enriched_brands = await fetch_all_raw_ads(categories_data, additional_url="?sort_by=newest")

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-28
Version: 1.0.0    
"""

import asyncio
from aiohttp import ClientSession
from tqdm import tqdm

from config import AIOHTTP_CLIENT
from parsers.products_links_parser import(
    parse_amount_of_products_links_next_data_json, 
    parse_products_links_next_data_json
)
from settings import LOGGER
from config import BASE_URL

from tqdm.std import tqdm as TqdmType
from typing import(
    Any,
    Coroutine,
    List
)
from data_types.raw_types import(
    RawBrand,
    RawFormat,
    RawModel,
    RawProduct
)


async def enrich_with_raw_ads_async(
    url: str,
    base_url: str
) -> List[RawProduct]:
    """
    Asynchronously fetch all raw product links from paginated pages at the given URL.

    - Fetches the first page to determine total number of pages.
    - Concurrently fetches all pages using aiohttp.
    - Parses product links from each page's HTML.
    - Displays a tqdm progress bar tracking page fetch completion.

    Args:
        url (str): The base URL to fetch paginated raw ads from.
        base_url (str): Base URL for parsing or logging context.

    Returns:
        List[RawProduct]: Aggregated list of raw product dictionaries collected from all pages.
                          Returns an empty list if fetching or parsing fails.
    """
    async with ClientSession() as session:
        try:
            html: str = await AIOHTTP_CLIENT.fetch_html(session, url)
            if html is None:
                LOGGER.warning(f"Failed to fetch HTML for {url}, returning empty list")
                return []

            page_count: int = parse_amount_of_products_links_next_data_json(html)
            if page_count == 0:
                LOGGER.warning(f"No pages found at {url}")
                return []

            LOGGER.info(f"Total pages found at {url}: {page_count}")

            page_bar: TqdmType = tqdm(
                total=page_count,
                desc="Pages",
                position=2,
                leave=False
            )

            tasks: List[Coroutine[Any, Any, str]] = [
                AIOHTTP_CLIENT.fetch_html(session, f"{url}&page={i}")
                for i in range(1, page_count + 1)
            ]

            ads: List[RawProduct] = []
            for coro in asyncio.as_completed(tasks):
                page_html: str = await coro
                if page_html:
                    ads.extend(parse_products_links_next_data_json(page_html, base_url))
                page_bar.update(1)

            page_bar.close()
            LOGGER.info(f"Found {len(ads)} product links from {url}")
            return ads

        except Exception as e:
            LOGGER.error(f"Error fetching product links from {url}: {e}", exc_info=True)
            return []
     

async def fetch_all_raw_ads(
    categories_data: RawFormat,
    additional_url: str,
) -> List[RawBrand]:
    """
    Traverse the brands and their models in the input categories_data,
    fetching raw product links asynchronously for each brand or model.

    - Displays a tqdm progress bar for brands (position=0).
    - For brands with models, displays a nested tqdm for models (position=1).
    - Uses enrich_with_raw_ads_async() to fetch paginated product links per model or brand URL.
    - Updates the brand and model dictionaries in place with a "product_links" key.

    Args:
        categories_data (RawFormat): Raw data containing brands and models.
        additional_url (str): URL query parameters to append to each product URL.

    Returns:
        List[RawBrand]: The modified list of brands enriched with product links.
    """
    brands: List[RawBrand] = categories_data.get("brands", [])

    brand_bar: TqdmType = tqdm(brands, desc="Brands", position=0)

    for brand in brand_bar:
        brand: RawBrand
        models: List[RawModel] = brand.get("models", [])
        brand_bar.set_description(f"Processing brand: {brand['name']} ({len(models)} models)")

        if not models:
            LOGGER.info(f"No models for brand: {brand['name']}, fetching from brand URL")
            product_url: str = brand.get("url", "")
            if additional_url:
                product_url += additional_url

            brand["product_links"] = await enrich_with_raw_ads_async(
                url=product_url,
                base_url=BASE_URL
            )

            LOGGER.info(f"Found {len(brand['product_links'])} products for brand: {brand['name']}")
        else:
            model_bar: TqdmType = tqdm(models, desc=f"{brand['name']} models", position=1, leave=False)

            for model in model_bar:
                model: RawModel
                product_url: str = model.get("url", "")
                if additional_url:
                    product_url += additional_url

                model["product_links"] = await enrich_with_raw_ads_async(
                    url=product_url,
                    base_url=BASE_URL
                )

            model_bar.close()      
            brand_bar.refresh()

            LOGGER.info(f"Found products for brand: {brand['name']}")

    brand_bar.close()
    return brands
