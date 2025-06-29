"""
src/main.py

This is the entry point of the parsing pipeline. It either loads previously saved raw data
or triggers the full data extraction pipeline, followed by cleaning and saving the results.

Main Workflow:
- Load existing raw data from disk (if CLEAN_ONLY is True).
- Otherwise, fetch data from lalafo.kg using asynchronous/synchronous clients.
- Clean the parsed raw data by removing or simplifying unnecessary fields.
- Save raw and cleaned data to JSON and/or compressed ZIP files.
- Log request statistics if enabled.

Author: Сh.Danil
Created: 2025-06-29
Last Modified: 2025-06-29
Version: 1.0.0
"""

import asyncio
from services.cleaning_service import clean_parsed_data
from services.raw_data_pipeline import get_raw_data
from utils.client_utils import log_client_request_counts
from utils.json_utils import load_existing_data, save_data
from utils.zip_utils import save_data_as_zip
from settings import LOGGER
from config import(
    AIOHTTP_CLIENT, 
    REQUESTS_CLIENT
)
from config import(
    SHOULD_SHOW_STATISTICS, 
    SHOULD_SAVE_RAW_DATA, 
    SHOULD_SAVE_CLEANED_DATA, 
    SHOULD_SAVE_CLEANED_DATA_AS_ZIP, 
    SHOULD_SAVE_RAW_DATA_AS_ZIP, 
    CLEAN_ONLY
)
from config import(
    RAW_DATA_PATH, 
    CLEANED_DATA_PATH, 
    RAW_DATA_ZIP_FILE_NAME, 
    RAW_DATA_ZIP_PATH, 
    CLEANED_DATA_ZIP_PATH
)
from config import CLEANED_DATA_ZIP_FILE_NAME
from data_types.cleaned_types import CleanedFormat
from data_types.raw_types import RawFormat


async def main():
    LOGGER.info("===== Starting Lalafo KG Parsing Pipeline =====")

    if CLEAN_ONLY:
        LOGGER.info("CLEAN_ONLY is True — loading existing raw data from file")
        raw_data: RawFormat = load_existing_data(RAW_DATA_PATH)
    else:
        LOGGER.info("CLEAN_ONLY is False — starting full parsing pipeline")
        raw_data: RawFormat = await get_raw_data()

        if SHOULD_SAVE_RAW_DATA:
            LOGGER.info("Saving raw data is enabled")
            if SHOULD_SAVE_RAW_DATA_AS_ZIP:
                LOGGER.info("Saving raw data as ZIP")
                save_data_as_zip(RAW_DATA_ZIP_PATH, raw_data, RAW_DATA_ZIP_FILE_NAME)
            save_data(RAW_DATA_PATH, raw_data)

    LOGGER.info("Cleaning parsed data")
    cleaned_data: CleanedFormat = clean_parsed_data(raw_data)

    if SHOULD_SAVE_CLEANED_DATA:
        LOGGER.info("Saving cleaned data is enabled")
        if SHOULD_SAVE_CLEANED_DATA_AS_ZIP:
            LOGGER.info("Saving cleaned data as ZIP")
            save_data_as_zip(CLEANED_DATA_ZIP_PATH, cleaned_data, CLEANED_DATA_ZIP_FILE_NAME)
        save_data(CLEANED_DATA_PATH, cleaned_data)

    if not CLEAN_ONLY and SHOULD_SHOW_STATISTICS:
        LOGGER.info("Logging request statistics")
        log_client_request_counts(AIOHTTP_CLIENT, REQUESTS_CLIENT)

    LOGGER.info("===== Parsing Pipeline Finished =====")


if __name__ == "__main__":
    asyncio.run(main())
