import asyncio
import json
from browser.selenium_client import SeleniumClient
from config import URL, BASE_URL, logger
from pathlib import Path
from parsers.category_parser import parse_categories
from parsers.subcategory_parser import parse_subcategories
from tqdm import tqdm


def load_existing_data(path: Path) -> list[dict]:
    if path.exists():
        logger.info(f"Found existing file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    logger.info("No existing file found. Will create new data.")
    return []


def save_data(path: Path, data: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Data saved to file: %s", path)


async def main():
    logger.info("Starting main parsing process")
    selenium: SeleniumClient = SeleniumClient(headless=True, wait_time=2.0)

    data_path = Path("src/data/categories_with_subcategories.json")
    categories = load_existing_data(data_path)

    try:
        if not categories:
            logger.info(f"Fetching main page HTML from {URL}")
            html = selenium.get_html(URL, wait_for_selector="nav.category-tab-list a.item_category")

            logger.info("Parsing categories from main page HTML")
            categories = parse_categories(html, BASE_URL)
            for cat in categories:
                cat["subcategories_loaded"] = False
            save_data(data_path, categories)
            logger.info(f"Found {len(categories)} categories")

        for category in tqdm(categories, desc="Fetching subcategories"):
            if category.get("subcategories_loaded"):
                logger.info(f"Skipping already loaded category: {category['brand']}")
                continue

            try:
                logger.info(f"Fetching subcategories for category '{category['brand']}' from {category['brand_url']}")
                sub_html = selenium.get_html(category["brand_url"], wait_for_selector="nav.category-tab-list a.item_param")
                subcats = parse_subcategories(sub_html, BASE_URL)
                category["subcategories"] = subcats
                category["subcategories_loaded"] = True
                logger.info(f"Found {len(subcats)} subcategories for category '{category['brand']}'")
            except Exception as e:
                logger.error(f"Failed to fetch subcategories for {category['brand']}: {e}", exc_info=True)
                category["subcategories"] = []
                category["subcategories_loaded"] = False
            finally:
                save_data(data_path, categories) 

    except Exception as e:
        logger.error(f"Error during Selenium processing: {e}", exc_info=True)
    finally:
        selenium.close()
        logger.info("Selenium WebDriver closed")


if __name__ == "__main__":
    asyncio.run(main())



        # soup = BeautifulSoup(html, "html.parser")
        # pretty_html = soup.prettify()

        # Path("src/data").mkdir(exist_ok=True)
        # file_path = Path("src/data") / "page.html"
        # with open(file_path, "w", encoding="utf-8") as f:
        #     f.write(pretty_html)
        # print(f"HTML сохранён в файл: {file_path}")
