"""
src/config.py

This module contains configuration constants for the web scraping project,
including URLs, HTTP client instances, file paths, flags, and data processing fields.

Constants:
- URL: The main listing URL for used cars on lalafo.kg.
- BASE_URL: Base domain URL for building absolute URLs.
- AIOHTTP_CLIENT: Asynchronous HTTP client instance with configured retries and timeout.
- REQUESTS_CLIENT: Synchronous HTTP client instance with configured retries and timeout.
- SORT_METHOD: Query parameter to sort listings by newest.
- TEMP_DATA_PATH, RAW_DATA_PATH, CLEANED_DATA_PATH: Paths for storing temporary, raw, and cleaned JSON data.
- RAW_DATA_ZIP_PATH, CLEANED_DATA_ZIP_PATH: Paths for storing compressed zip archives of data.
- RAW_DATA_ZIP_FILE_NAME, CLEANED_DATA_ZIP_FILE_NAME: Filenames inside zip archives.
- SHOULD_SAVE_RAW_DATA, SHOULD_SAVE_CLEANED_DATA, etc.: Boolean flags controlling data saving and processing behavior.
- COPY_TO_DETAILS_IF_EMPTY: List of fields to copy into details if empty.
- FIELDS_TO_REMOVE_TO_SIMLIFY: List of fields to remove to simplify data before processing.

Author: Сh.Danil
Created: 2025-06-29
Version: 1.0.0
"""

from browser.aiohttp_client import AiohttpClient
from browser.requests_client import RequestsClient
from typing import List

# URLs
URL: str = "https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom"
BASE_URL: str = "https://lalafo.kg"

# HTTP clients
AIOHTTP_CLIENT: AiohttpClient = AiohttpClient(delay_between_requests=0, retries=10, timeout=15)
REQUESTS_CLIENT: RequestsClient = RequestsClient(delay_between_requests=0, timeout=15, retries=10)

# Sorting
SORT_METHOD: str = "?sort_by=newest" 

# Paths
TEMP_DATA_PATH: str = "src/data/temp_data.json"
RAW_DATA_PATH: str = "src/data/raw_data.json"
CLEANED_DATA_PATH: str = "src/data/cleaned_data.json"
RAW_DATA_ZIP_PATH: str = "src/data/raw.zip"
CLEANED_DATA_ZIP_PATH: str = "src/data/cleaned.zip"

# Archive filenames inside zips
RAW_DATA_ZIP_FILE_NAME: str = "raw_data.json"
CLEANED_DATA_ZIP_FILE_NAME: str = "cleaned_data.json"

# Flags
SHOULD_SAVE_RAW_DATA: bool = False
SHOULD_SAVE_CLEANED_DATA: bool = True
SHOULD_SAVE_RAW_DATA_AS_ZIP: bool = True
SHOULD_SAVE_CLEANED_DATA_AS_ZIP: bool = True
SHOULD_SHOW_STATISTICS: bool = True
CLEAN_ONLY: bool = True
SHOULD_USE_TEMP_DATA: bool = True

# Fields and data processing
COPY_TO_DETAILS_IF_EMPTY: List[str] = ["description", "tracking_info"]
FIELDS_TO_REMOVE_TO_SIMLIFY: List[str] = [
    "id", "old_id", "title", "is_negotiable", "is_vip",
    "is_premium", "is_select", "currency", "symbol", "views", "impressions",
    "favorite_count", "callers_count", "writers_count", "category_id",
    "city_id", "city", "user_id", "user_ids", "origin_user_id", "country_id",
    "price", "old_price", "lat", "lng", "mobile", "images", "hide_phone",
    "hide_chat", "status_id", "can_free_push", "url", "created_time",
    "updated_time", "score_order", "is_freedom", "response_type", "campaign_show",
    "is_ppv", "price_type", "national_price", "national_old_price", "is_identity",
    "params", "user"
] + COPY_TO_DETAILS_IF_EMPTY
