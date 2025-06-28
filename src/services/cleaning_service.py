"""
cleaning_service.py

Module for high-level cleaning and normalization of raw advertisement data parsed from web sources.

This module provides functions to:
- Remove duplicate ads within each model
- Clean up product fields and discard unnecessary keys
- Normalize and simplify the data structure for further processing

Author: Сh.Danil
Created: 2025-06-25
Last Modified: 2025-06-28
Version: 1.0.0

Usage:
    from services.cleaning_service import clean_parsed_data
"""

from utils.ad_cleaning_utils import (
    simplify_structure, 
    remove_duplicate_products_within_models
)
from settings import LOGGER
from data_types.raw_types import RawFormat
from data_types.cleaned_types import CleanedFormat


def clean_parsed_data(raw_data: RawFormat) -> CleanedFormat:
    """
    Clean and simplify parsed advertisement data.

    This function performs two primary cleaning steps:
    1. Removes duplicate product entries within each model.
    2. Simplifies and normalizes the structure of each product,
       removing unnecessary fields and formatting the data consistently.

    Args:
        raw_data (RawFormat): The raw parsed data containing brands, models, and product entries.

    Returns:
        CleanedFormat: A cleaned and simplified version of the input data,
        structured according to the CleanedFormat type.
    """
    LOGGER.info("Starting data cleaning process")

    LOGGER.info("Removing duplicate products within models")
    remove_duplicate_products_within_models(raw_data)

    LOGGER.info("Cleaning product fields and removing unused keys")
    cleaned_data: CleanedFormat = simplify_structure(raw_data)

    LOGGER.info("Data cleaning completed")

    return cleaned_data
