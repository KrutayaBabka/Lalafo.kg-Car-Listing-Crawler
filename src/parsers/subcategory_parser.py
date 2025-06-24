from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import logger  # импорт логгера

def parse_subcategories(html: str, base_url: str) -> list[dict]:
    logger.info("Parsing subcategories from HTML content")
    soup = BeautifulSoup(html, 'html.parser')
    subcategories = []

    subcategory_links = soup.select("nav.category-tab-list a.item_param")
    logger.info("Found %d subcategory links", len(subcategory_links))

    for a in subcategory_links:
        name_tag = a.find('p', class_='LFParagraph')
        name = name_tag.text.strip() if name_tag else a.text.strip()
        href = a.get('href')
        full_url = urljoin(base_url, href) if href else None

        if name and full_url:
            subcategories.append({"model": name, "model_url": full_url})
            logger.debug("Parsed subcategory: %s -> %s", name, full_url)
        else:
            logger.warning("Skipped subcategory link due to missing name or URL")

    logger.info("Parsed total %d subcategories", len(subcategories))
    return subcategories
