"""
products_links_parser.py

This module is responsible for extracting product link data and the total number of
pagination pages from the embedded __NEXT_DATA__ JSON structure in lalafo.kg HTML pages.

Main Functions:
- parse_products_links_next_data_json: Extracts list of product dictionaries with absolute URLs.
- parse_amount_of_products_links_next_data_json: Determines how many pages of products exist.

Dependencies:
- BeautifulSoup: Used for locating and parsing embedded JSON in <script> tags.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.1
"""

import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup 
from settings import LOGGER 
from bs4 import Tag
from typing import(
    Any, 
    Dict, 
    List, 
    Optional
)
from data_types.raw_types import(
    RawFormat, 
    RawProduct
)


def parse_products_links_next_data_json(html: str, base_url: str) -> List[RawProduct]:
    """
    Parses the HTML content and extracts product link data from the embedded __NEXT_DATA__ JSON.

    Args:
        html (str): The raw HTML content of the model or brand product listing page.
        base_url (str): The base URL to convert relative product URLs to absolute URLs.

    Returns:
        List[RawProduct]: A list of product dictionaries with enriched absolute "url" fields.

    Raises:
        ValueError: If the expected script tag or JSON structure is missing or malformed.
    """
    LOGGER.info("Extracting selected model products links data from __NEXT_DATA__")

    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    script_tag: Optional[Tag] = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag or not script_tag.string:
        LOGGER.error("Script tag with id='__NEXT_DATA__' not found or empty")
        raise ValueError("Script tag with id='__NEXT_DATA__' not found")

    try:
        raw_json: str = script_tag.string
        data: Dict[str, Any] = json.loads(raw_json)
        items: List[RawProduct] = data["props"]["initialState"]["listing"]["listingFeed"]["data"]["items"]

        for item in items:
            relative_url: Optional[str] = item.get("url")
            if relative_url:
                item["url"] = urljoin(base_url, relative_url)
            else:
                LOGGER.warning(f"Item {item} does not have a 'url' field")

        LOGGER.info(f"Found {len(items)} model products in __NEXT_DATA__")

        return items

    except Exception as e:
        LOGGER.exception("Failed to parse model products: %s", e)
        return []
    

def parse_amount_of_products_links_next_data_json(html: str) -> int:
    """
    Parses the HTML content and returns the total number of pages available in the pagination meta.

    Args:
        html (str): The raw HTML content of the product listing page.

    Returns:
        int: Total number of pages (used for pagination). Defaults to 0 if not found or error occurs.

    Raises:
        ValueError: If the script tag with embedded JSON is not found or the structure is invalid.
    """
    LOGGER.info("Extracting amount of model products links data from __NEXT_DATA__")

    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    script_tag: Optional[Tag] = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag or not script_tag.string:
        LOGGER.error("Script tag with id='__NEXT_DATA__' not found or empty")
        raise ValueError("Script tag with id='__NEXT_DATA__' not found")

    try:
        raw_json: str = script_tag.string
        data: Dict[str, Any] = json.loads(raw_json)
        listing_data: Dict[str, Any] = data["props"]["initialState"]["listing"]["listingFeed"]["data"]

        page_count: int = listing_data.get("_meta", {}).get("pageCount", 0)
        return page_count

    except Exception as e:
        LOGGER.exception("Failed to parse product page count: %s", e)
        return 0
