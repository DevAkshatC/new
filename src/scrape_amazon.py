# src/scrape_amazon.py
import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import os

def scrape_amazon_reviews(product_url, max_pages=10):
    """
    Scrapes Amazon product reviews (multiple pages) and saves them to CSV.
    Returns list of review texts.
    """
    headers_list = [
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"},
        {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/110 Mobile Safari/537.36"},
    ]

    # Convert product page URL → review page
    if "/dp/" in product_url:
        asin = product_url.split("/dp/")[1].split("/")[0]
        product_url = f"https://www.amazon.in/product-reviews/{asin}"

    all_reviews = []

    for page in range(1, max_pages + 1):
        url = f"{product_url}?pageNumber={page}"
        headers = random.choice(headers_list)
        print(f"📄 Fetching page {page}: {url}")

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"❌ Request failed with {resp.status_code}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            review_divs = soup.find_all("span", {"data-hook": "review-body"})

            if not review_divs:
                print("⚠️ No reviews found on this page.")
                break

            for div in review_divs:
                text = div.get_text(strip=True)
                if len(text) > 20:
                    all_reviews.append(text)

            print(f"✅ Collected {len(all_reviews)} reviews so far...")
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print("⚠️ Error:", e)
            continue

    print(f"\n✅ Total reviews scraped: {len(all_reviews)}")

    # ✅ Save to CSV
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "scraped_reviews.csv")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    pd.DataFrame(all_reviews, columns=["review"]).to_csv(data_path, index=False)
    print(f"📁 Saved to: {data_path}")

    return all_reviews
