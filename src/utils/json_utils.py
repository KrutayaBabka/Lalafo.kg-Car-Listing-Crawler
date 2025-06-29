"""
src/utils/json_utils.py

This module provides utility functions for reading and writing JSON data
used throughout the data pipeline. It handles:
- Loading existing structured data from a JSON file.
- Saving updated or cleaned data back to disk.
- Logging all file interactions for traceability.

Functions:
- load_existing_data: Reads JSON data from a specified file path if it exists.
- save_data: Writes JSON-serializable data to a specified file path with formatting.


Author: Сh.Danil
Created: 2025-06-25
Last Modified: 2025-06-28
Version: 1.0.0   
"""

import json
from pathlib import Path
from typing import Any, List
from settings import LOGGER


def load_existing_data(path: str) -> List[dict[str, Any]]:
    """
    Load existing JSON data from a file.

    Args:
        path (str): Path to the JSON file to load.

    Returns:
        List[dict[str, Any]]: Parsed data from the file. Returns an empty list
        if the file does not exist.

    Logs:
        - INFO when file is found and loaded successfully.
        - INFO when file does not exist.
    """
    path: Path = Path(path)
    if path.exists():
        LOGGER.info(f"Found existing file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    LOGGER.info("No existing file found. Will create new data.")
    return []


def save_data(path: str, data: List[dict[str, Any]]) -> None:
    """
    Save JSON-serializable data to a file with UTF-8 encoding and pretty formatting.

    Args:
        path (str): Path to the file where data will be saved.
        data (List[dict[str, Any]]): List of dictionaries representing the data to save.

    Logs:
        - INFO upon successful file write.
    """
    path: Path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    LOGGER.info("Data saved to file: %s", path)
