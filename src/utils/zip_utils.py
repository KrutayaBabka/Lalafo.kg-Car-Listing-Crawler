"""
zip_utils.py

This module provides a utility function to compress JSON-serializable data into a ZIP file.

Main Function:
- save_data_as_zip: Serializes a list of dictionaries to JSON and stores it in a .zip archive.

Author: Сh.Danil
Created: 2025-06-29
Version: 1.0.0
"""

import json
import zipfile
from pathlib import Path
from typing import Any, List
from settings import LOGGER


def save_data_as_zip(zip_path: str, data: List[dict[str, Any]], json_filename: str = "data.json") -> None:
    """
    Save a list of dictionaries as a compressed JSON file inside a ZIP archive.

    Args:
        zip_path (str): Full path to the resulting ZIP file (e.g., "output/data.zip").
        data (List[dict[str, Any]]): List of dictionaries to serialize.
        json_filename (str): Name of the JSON file inside the archive (default: "data.json").

    Returns:
        None

    Logs:
        - INFO: Successful archive creation.
        - ERROR: If saving fails.
    """
    try:
        zip_path: Path = Path(zip_path)
        zip_path.parent.mkdir(parents=True, exist_ok=True)

        json_str: str  = json.dumps(data, ensure_ascii=False, indent=2)
        with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(json_filename, json_str)

        LOGGER.info(f"Data saved and compressed to ZIP file: {zip_path}")

    except Exception as e:
        LOGGER.error(f"Failed to save data to ZIP: {e}", exc_info=True)
