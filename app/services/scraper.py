from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from app.domain.entities.models import Platform
from typing import Optional, Dict
from urllib.parse import urljoin
import re

def scrape_platform(platform: Platform, query: str) -> Optional[Dict]:
    url = platform.search_url_template.format(query=query.replace(" ", "+"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(3000)
            html = page.content()
        except Exception as e:
            browser.close()
            print(f"[ERROR] Failed to load: {url}")
            return None
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    product = None

    # ========== ROZETKA ==========
    if platform.name.lower() == "rozetka":
        product = soup.select_one("rz-product-tile")
        if not product:
            return None

        title = product.select_one("a.tile-title")
        price = product.select_one("div.price")
        link = product.select_one("a[href]")

        return {
            "name_on_platform": title.text.strip() if title else "No title",
            "price": float(price.text.replace("₴", "").replace(" ", "").strip()) if price else None,
            "currency": "UAH",
            "rating": None,
            "reviews_count": None,
            "availability_status": "available",
            "url_on_platform": urljoin(platform.base_url, link["href"]) if link else None
        }

    # ========== OLX ==========
    elif platform.name.lower() == "olx":
        product = soup.select_one('[data-cy="l-card"]')
        if not product:
            return None

        title = product.select_one('[data-cy="ad-card-title"]')
        price = product.select_one('[data-testid="ad-price"]')
        link = product.select_one("a[href]")

        return {
            "name_on_platform": title.text.strip() if title else "No title",
            "price": float(re.sub(r"[^\d.]", "", price.text)) if price else None,
            "currency": "UAH",
            "rating": None,
            "reviews_count": None,
            "availability_status": "available",
            "url_on_platform": urljoin(platform.base_url, link["href"]) if link else None
        }

    # ========== PROM ==========
    elif platform.name.lower() == "prom":
        product = soup.select_one('[data-qaid="product_block"]')
        if not product:
            return None

        title = product.select_one('[data-qaid="product_name"]')
        price = product.select_one('[data-qaid="product_price"]')
        link = product.select_one("a[href]")

        return {
            "name_on_platform": title.text.strip() if title else "No title",
            "price": float(re.sub(r"[^\d.]", "", price.text)) if price else None,
            "currency": "UAH",
            "rating": None,
            "reviews_count": None,
            "availability_status": "available",
            "url_on_platform": urljoin(platform.base_url, link["href"]) if link else None
        }

    return None
