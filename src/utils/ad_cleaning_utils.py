"""
ad_cleaning_utils.py

This module contains utility functions to clean and normalize advertisement product data.
It is used during the data processing pipeline to simplify structures, remove redundancy,
and ensure consistency in product fields.

Main functionalities:
- Remove duplicate products within models based on their IDs
- Copy missing fields into nested product details if needed
- Remove unnecessary fields to reduce data size and simplify the structure

Used in:
- cleaning_service.clean_parsed_data

Dependencies:
- tqdm: Used to display progress bars during data processing

Author: Сh.Danil
Created: 2025-06-26
Last Modified: 2025-06-28
Version: 1.0.0
"""

from typing import (
    List, 
    Optional, 
    Set
)
from tqdm import tqdm

from settings import LOGGER
from config import (
    COPY_TO_DETAILS_IF_EMPTY, 
    FIELDS_TO_REMOVE_TO_SIMLIFY
)

from data_types.cleaned_types import CleanedFormat
from data_types.raw_types import (
    RawFormat, 
    RawBrand, 
    RawModel, 
    RawProduct, 
    RawProductDetails
)


def clean_product_fields(product: RawProduct) -> None:
    """
    Clean and normalize fields within a single product entry.

    - Copies specific fields into `product_details` if they are missing there.
    - Removes unnecessary fields from the top-level product dictionary.

    Args:
        product (RawProduct): A dictionary representing a single product and its details.

    Returns:
        None. The product is modified in-place.
    """
    product_details: RawProductDetails = product.get("product_details")
    if isinstance(product_details, dict):
        for field in COPY_TO_DETAILS_IF_EMPTY:
            if field in product and not product_details.get(field):
                product_details[field] = product[field]
                LOGGER.debug(f"Copied '{field}' from product to product_details")

    for field in FIELDS_TO_REMOVE_TO_SIMLIFY:
        if field in product:
            product.pop(field, None)
            LOGGER.debug(f"Removed '{field}' from product")


def simplify_structure(data: RawFormat) -> CleanedFormat:
    """
    Simplify and normalize the structure of parsed advertisement data.

    - Applies cleaning to each product in all brands and models.
    - Removes or restructures redundant fields.
    - Handles both model-level and brand-level product links.

    Args:
        data (RawFormat): Raw parsed advertisement data.

    Returns:
        CleanedFormat: The cleaned and simplified advertisement data.
    """
    brands: List[RawBrand] = data.get("brands", [])
    LOGGER.info(f"Simplifying structure for {len(brands)} brands")

    for brand in tqdm(brands, desc="Simplifying Brands", position=0):
        brand_name: str = brand.get("name", "UnknownBrand")
        LOGGER.debug(f"Cleaned brand '{brand_name}'")

        if brand.get("models", []):
            for model in tqdm(brand["models"], desc=f"Models ({brand_name})", leave=False, position=1):
                model_name: str = model.get("name", "UnknownModel")
                for product in model.get("product_links", []):
                    clean_product_fields(product)
                LOGGER.debug(f"Cleaned products in model '{model_name}' of brand '{brand_name}'")
        elif brand.get("product_links", []):
            for product in brand.get("product_links", []):
                clean_product_fields(product)
            LOGGER.debug(f"Cleaned products directly in brand '{brand_name}' (no models)")

    LOGGER.info("Simplification completed")
    return data
    

def remove_duplicate_products_within_models(data: RawFormat) -> None:
    """
    Remove duplicate product entries from each model in the dataset.

    A duplicate is defined as a product having the same 'id' as a previously seen product
    within the same model.

    Args:
        data (RawFormat): Raw advertisement data containing brands and models.

    Returns:
        None. Modifies the input data in-place.
    """
    brands: List[RawBrand] = data.get("brands", [])
    LOGGER.info(f"Checking for duplicate products in {len(brands)} brands")

    for brand in tqdm(brands, desc="Removing duplicates in brands", position=0):
        brand_name: str = brand.get("name", "UnknownBrand")
        models: List[RawModel] = brand.get("models", [])

        for model in tqdm(models, desc=f"Models ({brand_name})", position=1, leave=False):
            model_name: str = model.get("name", "UnknownModel")
            seen_ids: Set[int] = set()
            unique_products: List[RawProduct] = []

            for product in model.get("product_links", []):
                product_id: Optional[int] = product.get("id")
                if product_id is None:
                    LOGGER.warning(
                        f"No ID found in product for brand '{brand_name}', model '{model_name}'"
                    )
                    continue

                if product_id in seen_ids:
                    LOGGER.warning(
                        f"Duplicate product ID {product_id} found in brand '{brand_name}', model '{model_name}' — removing duplicate"
                    )
                    continue

                seen_ids.add(product_id)
                unique_products.append(product)

            before: int = len(model.get("product_links", []))
            after: int = len(unique_products)
            if before != after:
                LOGGER.info(
                    f"Removed {before - after} duplicates in brand '{brand_name}', model '{model_name}'"
                )

            model["product_links"] = unique_products