from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import logger 


def parse_categories(html: str, base_url: str) -> list[dict]:
    logger.info("Parsing categories from HTML content")
    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    
    category_links = soup.select("nav.category-tab-list a.item_category")
    logger.info("Found %d category links", len(category_links))
    
    for a in category_links:
        name_tag = a.find('p', class_='LFParagraph')
        name = name_tag.text.strip() if name_tag else a.text.strip()
        href = a.get('href')
        full_url = urljoin(base_url, href) if href else None
        
        if name and full_url:
            categories.append({"brand": name, "brand_url": full_url})
            logger.debug("Parsed category: %s -> %s", name, full_url)
        else:
            logger.warning("Skipped category link due to missing name or URL")
    
    logger.info("Parsed total %d categories", len(categories))
    return categories
