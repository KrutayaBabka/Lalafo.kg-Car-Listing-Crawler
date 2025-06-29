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

```

Lalafo.kg-Car-Listing-Crawler/
├── .gitignore
├── requirements.txt
├── README.md
├── venv/ (virtual environment — excluded from version control)
└── src/
├── main.py
├── config.py
├── settings.py
├── data/
│   └── references/
│       ├── raw\_reference.json        # Example of raw data structure
│       └── cleaned\_reference.json    # Example of cleaned data structure
├── browser/
│   ├── aiohttp\_client.py
│   └── requests\_client.py
├── data\_types/
│   ├── base\_types.py
│   ├── raw\_types.py
│   └── cleaned\_types.py
├── parsers/
│   ├── category\_parser.py
│   ├── subcategory\_parser.py
│   ├── product\_details\_parser.py
│   └── products\_links\_parser.py
├── services/
│   ├── raw\_data\_pipeline.py
│   ├── raw\_ads\_service.py
│   ├── ad\_details\_service.py
│   ├── subcategory\_service.py
│   └── cleaning\_service.py
└── utils/
├── json\_utils.py
├── zip\_utils.py
└── client\_utils.py

````

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