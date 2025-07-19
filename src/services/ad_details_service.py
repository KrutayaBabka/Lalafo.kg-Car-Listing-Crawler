"""
src/services/ad_details_service.py

Asynchronous service module to fetch and enrich detailed product data
from raw advertisement links using aiohttp for concurrent HTTP requests.

This module:
- Fetches HTML pages asynchronously for product detail URLs.
- Parses product details JSON data from fetched HTML.
- Enriches the original product data structure with detailed info.
- Uses nested tqdm progress bars for brands, models, and products,
  providing smooth console progress feedback during async operations.

Dependencies:
- aiohttp: for asynchronous HTTP client requests.
- tqdm: for progress bar visualization.

Typical usage:
    await enrich_all_product_details_async(raw_data)

Author: Сh.Danil
Created: 2025-06-26
Last Modified: 2025-06-28
Version: 1.0.0    
"""

import asyncio
from aiohttp import(
    ClientSession, 
    ClientTimeout
)
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from tqdm.std import tqdm as TqdmType
from typing import(
    Any, 
    Coroutine, 
    List
)

from config import AIOHTTP_CLIENT
from parsers.product_details_parser import parse_product_details_next_data_json
from settings import LOGGER
from data_types.raw_types import(
    RawBrand, 
    RawFormat, 
    RawModel, 
    RawProduct, 
    RawProductDetails
)


async def fetch_product_details(
    session: ClientSession,
    product_link: RawProduct,
    base_url: str
) -> RawProductDetails:
    """
    Fetch and parse detailed information for a single product asynchronously.

    Args:
        session (ClientSession): An aiohttp client session for making HTTP requests.
        product_link (RawProduct): A dictionary containing at least a 'url' key for the product.
        base_url (str): The base URL used for relative path resolution or logging.

    Returns:
        RawProductDetails: The input product_link dictionary updated with a
                          'product_details' field containing parsed details.
    """
    url: str = product_link.get("url", "")
    product_link["product_details"] = {}

    if not url:
        LOGGER.warning("No URL provided in product link, returning empty product details")
        return product_link

    html: str = await AIOHTTP_CLIENT.fetch_html(session, url)
    if html is None:
        LOGGER.warning(f"Failed to fetch HTML for {url}, returning empty product details")
        return product_link

    product_link["product_details"] = parse_product_details_next_data_json(html, base_url)
    return product_link


async def enrich_all_product_details_async(raw_data: RawFormat, base_url: str) -> None:
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        brands: List[RawBrand] = raw_data["brands"]
        brand_bar: TqdmType = tqdm(brands, desc="Brands", position=0)

        for brand in brand_bar:
            models: List[RawModel] = brand.get("models", [])
            brand_bar.set_description(f"Brand: {brand['name']} ({len(models)} models)")

            if models:
                model_bar: TqdmType = tqdm(models, desc="Models", position=1, leave=False)
                for model in model_bar:
                    product_links: List[RawProduct] = model.get("product_links", [])
                    model_bar.set_description(f"Model: {model['name']} ({len(product_links)} links)")

                    if product_links:
                        tasks = []
                        for product_link in product_links:
                            task = asyncio.create_task(fetch_product_details(session, product_link, base_url))
                            tasks.append((task, product_link))

                        product_bar: TqdmType = tqdm(total=len(product_links), desc="Products", position=2, leave=False)
                        for coro in asyncio.as_completed([t for t, _ in tasks]):
                            result = await coro
                            for t, product_link in tasks:
                                if t == coro:
                                    product_link.update(result)
                                    break
                            product_bar.update(1)
                        product_bar.close()
                    else:
                        LOGGER.warning(f"No product links for model: {model['name']} (brand: {brand['name']})")
                model_bar.close()
            else:
                product_links: List[RawProduct] = brand.get("product_links", [])
                if product_links:
                    tasks = []
                    for product_link in product_links:
                        task = asyncio.create_task(fetch_product_details(session, product_link, base_url))
                        tasks.append((task, product_link))

                    product_bar: TqdmType = tqdm(total=len(product_links), desc="Products (no models)", position=1, leave=False)
                    for coro in asyncio.as_completed([t for t, _ in tasks]):
                        result = await coro
                        for t, product_link in tasks:
                            if t == coro:
                                product_link.update(result)
                                break
                        product_bar.update(1)
                    product_bar.close()
                else:
                    LOGGER.warning(f"No product links for brand: {brand['name']}")
        brand_bar.close()
        LOGGER.info("✅ Finished fetching all product details.")
