"""
subcategory_parser.py

This module extracts subcategory (model) information from the embedded JSON
within the `__NEXT_DATA__` script tag on a brand category page.

Main Function:
- parse_subcategories_next_data_json: Extracts list of models from JSON data embedded in HTML.

Dependencies:
- BeautifulSoup: Used to locate the embedded script tag.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.0
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
    RawModel
)


def parse_subcategories_next_data_json(html: str, base_url: str) -> RawFormat:
    """
    Parse the given HTML to extract model subcategories from the `__NEXT_DATA__` script tag.

    Args:
        html (str): Raw HTML content of the brand category page.
        base_url (str): Base URL used to convert relative model URLs into absolute ones.

    Returns:
        RawFormat: A dictionary with a "models" key containing a list of model dictionaries.

    Raises:
        ValueError: If the expected JSON structure or script tag is missing or invalid.
    """
    LOGGER.info("Extracting selected subcategory data from __NEXT_DATA__")

    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    script_tag: Optional[Tag] = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag or not script_tag.string:
        LOGGER.error("Script tag with id='__NEXT_DATA__' not found or empty")
        raise ValueError("Script tag with id='__NEXT_DATA__' not found")

    try:
        raw_json: str = script_tag.string
        data: Dict[str, Any] = json.loads(raw_json)

        section: Dict[str, Any] = (
            data.get("props", {})
            .get("initialState", {})
            .get("listing", {})
            .get("listingLinkSection", {})
        )

        items: List[Dict[str, Any]] = section.get("items", [])
        models: List[RawModel] = []

        for item in items:
            relative_url: Optional[str] = item.get("url")
            full_url: Optional[str] = urljoin(base_url, relative_url) if relative_url else None

            model: RawModel = {
                "id": item.get("id"),
                "name": item.get("name"),
                "url": full_url,
            }
            models.append(model)

        LOGGER.info("Extracted %d models from listingLinkSection", len(models))

        return {
            "models": models
        }

    except Exception as e:
        LOGGER.exception("Failed to extract selected subcategory data: %s", e)
        raise ValueError("Failed to extract selected subcategory data") from e
