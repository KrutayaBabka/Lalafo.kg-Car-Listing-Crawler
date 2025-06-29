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

## 📁 Project Structure

src/
│
├── main.py                    # Entry point
├── config.py                  # Global constants & logging
│
├── services/
│   └── crawl_service.py       # Orchestrates crawling & data saving
│
├── utils/
│   ├── __init__.py            # Re-exports key helpers
│   ├── fetch.py               # Synchronous HTML fetcher
│   ├── pagination.py          # Page-count & URL builder
│   ├── parse_listings.py      # Extracts links from listing cards
│   └── parse_details/         # Fine-grained extractors
│       ├── __init__.py
│       ├── average_price.py
│       ├── breadcrumbs.py
│       ├── configuration.py
│       ├── contact.py
│       ├── credit.py
│       ├── head_info.py
│       ├── history.py
│       ├── images.py
│       ├── seller_comment.py
│       ├── specs.py
│       └── vin.py
│
└── data/
    └── reference_data/        # Sample HTML pages & expected JSON output
                               # Handy for tests / debugging
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