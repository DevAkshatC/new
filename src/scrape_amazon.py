# src/scrape_amazon.py

import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import os


def scrape_amazon_reviews(product_url, max_pages=10):
    """
    Scrapes Amazon reviews from multiple pages.
    Returns: list of review strings.
    """

    # Header rotation to avoid Amazon blocking requests
    headers_list = [
        {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                           " AppleWebKit/537.36 (KHTML, like Gecko)"
                           " Chrome/129.0 Safari/537.36"),
            "Accept-Language": "en-IN,en;q=0.9"
        },
        {
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                           " AppleWebKit/605.1.15 (KHTML, like Gecko)"
                           " Version/17.3 Safari/605.1.15"),
            "Accept-Language": "en-IN,en;q=0.9"
        }
    ]

    # ✅ Convert product page → review page
    asin = None
    if "/dp/" in product_url:
        asin = product_url.split("/dp/")[1].split("/")[0]
    elif "/product-reviews/" in product_url:
        asin = product_url.split("/product-reviews/")[1].split("/")[0]

    if not asin:
        print("❌ Invalid Amazon product link!")
        return []

    base_review_url = f"https://www.amazon.in/product-reviews/{asin}"

    all_reviews = []

    print(f"\n🔍 Scraping Amazon reviews for ASIN: {asin}")

    for page in range(1, max_pages + 1):
        url = f"{base_review_url}?pageNumber={page}"
        print(f"➡ Fetching page {page}")

        try:
            resp = requests.get(url, headers=random.choice(headers_list), timeout=20)

            if resp.status_code != 200:
                print(f"❌ HTTP {resp.status_code} → Page Skipped")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            review_blocks = soup.find_all("span", {"data-hook": "review-body"})

            if not review_blocks:
                print("⚠ No more reviews found. Stopping.")
                break

            for block in review_blocks:
                text = block.get_text(separator=" ", strip=True)
                if len(text) > 15:
                    all_reviews.append(text)

            print(f"✅ Total collected so far: {len(all_reviews)}")

            time.sleep(random.uniform(1.5, 3.0))  # Anti-bot delay

        except Exception as e:
            print(f"⚠ Error on page {page}: {e}")
            continue

    print(f"\n✅ Finished scraping. Total reviews: {len(all_reviews)}")

    # ✅ Save CSV into /data/scraped_reviews.csv
    data_path = os.path.join(os.path.dirname(os.path.dirname(_file_)), "data", "scraped_reviews.csv")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    pd.DataFrame(all_reviews, columns=["review"]).to_csv(data_path, index=False)

    print(f"📁 Saved to: {data_path}")

    return all_reviews
