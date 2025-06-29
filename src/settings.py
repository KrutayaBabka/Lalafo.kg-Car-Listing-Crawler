"""
src/settings.py

This module sets up logging configuration and HTTP headers
used across the scraping project.

Constants:
- HEADERS: Dictionary with HTTP headers including User-Agent for requests.
- LOGGER: Configured logger instance for the project.

Logging:
- Logs are saved to 'app.log' in append mode.
- Log format includes timestamp, log level, and message.
- Default log level is INFO.

Author: Сh.Danil
Created: 2025-06-29
Version: 1.0.0
"""

import logging
from typing import Dict

# HTTP headers used for all requests
HEADERS: Dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Logging configuration
# - Log file: 'app.log'
# - Mode: append
# - Format: timestamp + log level + message
# - Level: INFO
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# Global logger instance
LOGGER: logging.Logger = logging.getLogger(__name__)