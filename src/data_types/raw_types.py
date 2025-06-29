"""
src/data_types/raw_types.py

This module defines raw (unprocessed) TypedDict data structures that extend base types
to represent the raw data formats parsed directly from the source JSON or HTML.

These raw types allow optional fields and nested structures like products within models
and brands, to facilitate stepwise parsing and processing.

Author: Сh.Danil
Created: 2025-06-27
Last Modified: 2025-06-29
Version: 1.0.0
"""

from typing import(
    Optional, 
    List
)
from data_types.base_types import(
    BaseAttributes, 
    BaseProductAttributes, 
    Brand, 
    Format, 
    Model, 
    ProductDetails, 
    TrackingInfo, 
    User
)


class RawProductDetails(ProductDetails, total=False):
    tracking_info: Optional[List]


class RawProduct(BaseAttributes, BaseProductAttributes, total=False):
    user: Optional[User]
    params: Optional[List]
    tracking_info: Optional[List[TrackingInfo]]
    product_details: Optional[RawProductDetails]


class RawModel(Model, total=False):
    product_links: Optional[List[RawProduct]]


class RawBrand(Brand, total=False):
    models: Optional[List[RawModel]]
    product_links: Optional[List[RawProduct]]


class RawFormat(Format, total=False):
    brands: Optional[List[RawBrand]]