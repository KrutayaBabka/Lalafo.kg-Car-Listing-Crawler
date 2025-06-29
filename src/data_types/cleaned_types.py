"""
cleaned_types.py

This module defines cleaned TypedDict data structures representing processed and
normalized data after cleaning and simplifying the raw parsed data.

These cleaned types remove unnecessary fields and standardize the structure,
ready for downstream processing or storage.

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
    BaseProductAttributes, 
    Brand, 
    Format, 
    Model, 
    ProductDetails, 
    TrackingInfo
)


class CleanedProductDetails(ProductDetails, total=False):
    tracking_info: Optional[List[TrackingInfo]]


class CleanedProduct(BaseProductAttributes, total=False):    
    product_details: Optional[CleanedProductDetails]


class CleanedModel(Model, total=False):
    product_links: Optional[List[CleanedProduct]]


class CleanedBrand(Brand, total=False):
    models: Optional[List[CleanedModel]]
    product_links: Optional[List[CleanedProduct]]


class CleanedFormat(Format, total=False):
    brands: Optional[List[CleanedBrand]]