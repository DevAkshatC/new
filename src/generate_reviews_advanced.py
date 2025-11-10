# generate_reviews_advanced.py
import pandas as pd
import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker()

# --- Step 1: Base templates for fake & real reviews ---
real_reviews = [
    "I absolutely love this product! Works perfectly.",
    "Fast delivery and excellent quality.",
    "Very satisfied, will buy again.",
    "Item as described, happy with purchase.",
    "Great customer service, very helpful.",
    "High quality, exactly what I needed.",
    "Received the product on time, works well.",
    "Five stars, highly recommend!",
    "Product exceeded my expectations.",
    "Excellent packaging and quick shipping."
]

fake_reviews = [
    "This is a fake product, do not buy.",
    "Scam! Paid for nothing.",
    "Fake review, they gave me free product.",
    "Terrible product, completely fake.",
    "Awful experience, do not trust.",
    "Fraudulent seller, item never arrived.",
    "Fake item, very disappointed.",
    "Product is fake, not as described.",
    "Received a fake product, warning!",
    "This is a scam, waste of money."
]

# --- Step 2: Generate enhanced dataset ---
data = []
for i in range(500):  # 500 real + 500 fake = 1000 total
    # Generate real review
    real_review = random.choice(real_reviews)
    real_username = fake.user_name()
    real_date = fake.date_between(start_date='-2y', end_date='today')
    real_rating = random.randint(4, 5)
    data.append({
        'username': real_username,
        'review': real_review,
        'label': 'real',
        'rating': real_rating,
        'date': real_date
    })

    # Generate fake review
    fake_review = random.choice(fake_reviews)
    fake_username = fake.user_name()
    fake_date = fake.date_between(start_date='-2y', end_date='today')
    fake_rating = random.randint(1, 2)
    data.append({
        'username': fake_username,
        'review': fake_review,
        'label': 'fake',
        'rating': fake_rating,
        'date': fake_date
    })

# --- Step 3: Save dataset ---
df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle rows
df.to_csv('../data/reviews_advanced.csv', index=False)

print("✅ Enhanced dataset created successfully at: ../data/reviews_advanced.csv")
print(f"Total reviews: {len(df)}")
print(df.head(10))
