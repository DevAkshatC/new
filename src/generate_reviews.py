# src/generate_reviews.py
import random
import pandas as pd
import os

# Templates
real_templates = [
    "I absolutely love this {product}! Works perfectly.",
    "Fast delivery and excellent {feature}.",
    "Very satisfied, will buy again.",
    "Item as described, happy with the {product}.",
    "Great customer service and support.",
    "High quality, exactly what I needed.",
    "Received the product on time, works well.",
    "Five stars, highly recommend!",
    "Product exceeded my expectations.",
    "Excellent packaging and quick shipping."
]

fake_templates = [
    "This is a fake {product}, do not buy.",
    "Scam! Paid for nothing.",
    "Fake review, they gave me free {product}.",
    "Terrible product, completely fake.",
    "Awful experience, do not trust.",
    "Fraudulent seller, item never arrived.",
    "Fake item, very disappointed.",
    "Product is fake, not as described.",
    "Received a fake product, warning!",
    "This is a scam, waste of money."
]

products = ["phone", "laptop", "charger", "headphone", "watch", "camera", "tablet", "speaker", "microwave", "printer"]
features = ["performance", "design", "battery life", "display", "sound quality", "durability", "speed", "comfort", "fit", "resolution"]

def generate_reviews(n=1000):
    reviews = []
    for _ in range(n):
        if random.random() < 0.5:
            template = random.choice(real_templates)
            label = "real"
        else:
            template = random.choice(fake_templates)
            label = "fake"
        review = template.format(product=random.choice(products), feature=random.choice(features))
        reviews.append({"review": review, "label": label})
    return pd.DataFrame(reviews)

if __name__ == "__main__":
    # BASE_DIR = folder containing this script (src)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # ROOT_DIR = project root (one level up from src)
    ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
    os.makedirs(os.path.join(ROOT_DIR, "data"), exist_ok=True)

    df = generate_reviews(1000)
    out_path = os.path.join(ROOT_DIR, "data", "reviews_large.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Generated {len(df)} reviews -> {out_path}")
    # quick existence check
    print("Exists:", os.path.exists(out_path))
    print(df.head())
