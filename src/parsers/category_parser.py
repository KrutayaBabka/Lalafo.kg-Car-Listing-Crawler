"""
category_parser.py

This module is responsible for parsing the root category page HTML and extracting
brand information from the embedded __NEXT_DATA__ JSON.

Main function:
- parse_categories_next_data_json: Extracts the category's brands and metadata.

Dependencies:
- BeautifulSoup: For locating embedded script tags.

Author: Сh.Danil
Created: 2025-06-26
Last Modified: 2025-06-29
Version: 1.0.0
"""

from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from settings import LOGGER 
from typing import(
    Any, 
    Dict, 
    List, 
    Optional
)
from data_types.raw_types import(
    RawBrand, 
    RawFormat
)
from bs4 import Tag
 

def parse_categories_next_data_json(html: str, base_url: str) -> RawFormat:
    """
    Parse the provided HTML and extract category information from __NEXT_DATA__ script tag.

    Args:
        html (str): Raw HTML content of the category page.
        base_url (str): The base URL to prepend to relative brand links.

    Returns:
        RawFormat: A dictionary with 'ads_count' and list of brand entries under 'brands'.

    Raises:
        ValueError: If the required script tag or expected JSON structure is missing or invalid.
    """
    LOGGER.info("Extracting selected category data from __NEXT_DATA__")
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')

    script_tag: Optional[Tag] = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script_tag:
        LOGGER.error("Script tag with id='__NEXT_DATA__' not found")
        raise ValueError("Script tag with id='__NEXT_DATA__' not found")

    try:
        raw_json: str = script_tag.string
        data: Dict[str, Any] = json.loads(raw_json)

        selected: Dict[str, Any] = data["props"]["initialState"]["listing"]["selectedCategory"]
        ads_count: int = int(selected.get("ads_count"))
        raw_children: List[Dict[str, Any]] = selected.get("children", [])

        children: List[RawBrand] = []
        for child in raw_children:
            relative_url: Optional[str] = child.get("url")
            url: Optional[str] = base_url + relative_url if relative_url else None
            children.append({
                "id": child.get("id"),
                "name": child.get("name"),
                "ads_count": child.get("ads_count"),
                "url": url,
                "image": child.get("image"),
                "singular_name": child.get("singular_name"),
            })

        LOGGER.info("Selected category ads_count: %s, brands: %d", ads_count, len(children))

        return {
            "ads_count": ads_count,
            "brands": children
        }

    except Exception as e:
        LOGGER.exception("Failed to extract selected category data: %s", e)
        raise ValueError("Failed to extract selected category data") from e