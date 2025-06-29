```markdown
# 🚗 Lalafo.kg Used Cars Parser

A scalable, asynchronous web scraping pipeline for extracting, cleaning, and storing structured advertisement data from [lalafo.kg](https://lalafo.kg). This project is tailored to scrape used car listings, parse detailed advertisement metadata, and provide cleaned JSON outputs ready for analysis or integration.

## 📌 Features

- Fully asynchronous and concurrent data extraction with fallback mechanisms.
- Clean, modular architecture for scraping, parsing, and cleaning.
- Reusable data types using `TypedDict`.
- Robust error handling with automatic retries and logging.
- JSON + ZIP data export with cleaned and raw dataset variants.
- Multi-level CLI progress bars using `tqdm`.
- Configurable and environment-independent setup.

---

```
```
## 📁 Project Structure

src/
│
├── main.py                    # Entry point of the parsing pipeline
├── config.py                  # Configuration constants, URLs, flags
├── settings.py                # Logger setup and HTTP headers
│
├── services/                  # Core async services for crawling and processing
│   ├── raw_data_pipeline.py   # Orchestrates full raw data parsing workflow
│   ├── raw_ads_service.py     # Fetches raw ads concurrently
│   ├── ad_details_service.py  # Fetches and enriches product details async
│   ├── subcategory_service.py # Handles subcategory (model) enrichment
│   └── cleaning_service.py    # Cleans and normalizes raw parsed data
│
├── utils/                     # Helper utilities for JSON, ZIP, HTTP logging
│   ├── client_utils.py        # Request counts logging helpers
│   ├── json_utils.py          # JSON read/write helpers
│   └── zip_utils.py           # Save data as compressed ZIP archives
│
├── parsers/                   # HTML and JSON extraction modules
│   ├── category_parser.py
│   ├── subcategory_parser.py
│   ├── product_details_parser.py
│   └── products_links_parser.py
│
├── browser/                   # HTTP client wrappers (async & sync)
│   ├── aiohttp_client.py
│   └── requests_client.py
│
├── data/                      # Sample reference data (raw and cleaned)
│   └── references/
│       ├── raw_reference.json
│       └── cleaned_reference.json
│
└── data_types/                # TypedDict definitions for data models
├── base_types.py
├── raw_types.py
└── cleaned_types.py

```
---

## 🛠 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/KrutayaBabka/Lalafo.kg-Car-Listing-Crawler.git
cd Lalafo.kg-Car-Listing-Crawler
````

### 2. Create Virtual Environment

#### On Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the full pipeline:

```bash
python src/main.py
```

The pipeline will:

* Load raw data if available, or fetch it from lalafo.kg
* Clean and normalize it
* Save both raw and cleaned datasets to disk (`.json` and `.zip`)

You can configure behavior using flags inside `src/config.py`.

---

## 🧪 Data Output

| File                     | Description                           |
| ------------------------ | ------------------------------------- |
| `raw_reference.json`     | Sample of raw scraped data            |
| `cleaned_reference.json` | Sample of cleaned and simplified data |
| `*.json`                 | Full datasets saved to JSON format    |
| `*.zip`                  | Compressed versions of datasets       |

---

## Modules Overview

| Module        | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| `main.py`     | Entry point for parsing and cleaning.                                 |
| `config.py`   | Central configuration for paths, flags, clients.                      |
| `settings.py` | Logger and request headers setup.                                     |
| `browser/`    | Contains both `aiohttp` and `requests` client wrappers.               |
| `data_types/` | Structured `TypedDict` definitions for raw and cleaned data.          |
| `parsers/`    | Extract brand, model, product, and pagination metadata from HTML.     |
| `services/`   | Modular async logic for ads scraping, detail enrichment, and cleanup. |
| `utils/`      | JSON and ZIP helpers, request logging utilities.                      |

---

## 👤 Author

**Ch.Danil**
Created: June 29, 2025
Version: 1.0.0

---

## 📄 License

This project is licensed under the MIT License.

## 🙌 Contributing

Found a bug? Have an idea or improvement?
Pull requests and issues are very welcome! 
Thank you for helping improve this project!