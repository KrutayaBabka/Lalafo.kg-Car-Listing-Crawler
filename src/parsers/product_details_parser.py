"""
src/parsers/product_details_parser.py

This module is responsible for extracting detailed product information
from the embedded __NEXT_DATA__ JSON structure on lalafo.kg product pages.

Main Function:
- parse_product_details_next_data_json: Extracts full product details from the ad page.

Dependencies:
- BeautifulSoup: Used to locate and extract embedded script data.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.0
"""

import json
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from settings import LOGGER
from bs4 import Tag
from data_types.raw_types import RawProductDetails
from typing import(
    Any, 
    Dict, 
    Optional
)


def parse_product_details_next_data_json(html: str, base_url: str) -> RawProductDetails:
    """
    Parses the HTML content and extracts product details from the embedded __NEXT_DATA__ JSON.

    Args:
        html (str): Raw HTML content of the product detail page.
        base_url (str): Base URL to resolve relative product URLs.

    Returns:
        RawProductDetails: A dictionary containing detailed product information,
                           including resolved "url" field.

    Raises:
        ValueError: If parsing fails or the expected structure is missing.
    """
    LOGGER.info("Extracting product details from __NEXT_DATA__")

    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    script_tag: Optional[Tag] = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag or not script_tag.string:
        LOGGER.error("Script tag with id='__NEXT_DATA__' not found or empty")
        return {}

    try:
        raw_json: str = script_tag.string
        data: Dict[str, Any] = json.loads(raw_json)

        ad_details: Dict[str, Any] = data["props"]["initialState"]["feed"]["adDetails"]
        current_ad_id: str = str(ad_details.get("currentAdId", ""))

        product_data: RawProductDetails = ad_details.get(current_ad_id, {}).get("item", {})

        if "url" in product_data:
            product_data["url"] = urljoin(base_url, product_data["url"])
        else:
            product_data["url"] = None

        return product_data

    except Exception as e:
        LOGGER.exception("Failed to parse product details: %s", e)
        return {}
