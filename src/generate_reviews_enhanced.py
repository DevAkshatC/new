import pandas as pd
import random
import os
from faker import Faker

fake = Faker()

# ✅ Auto-detect project base folder (works anywhere)
base_path = os.path.dirname(os.path.dirname(__file__))  # one level up from src/
data_path = os.path.join(base_path, 'data', 'reviews.csv')
output_path = os.path.join(base_path, 'data', 'reviews_large_enhanced.csv')

print(f"📂 Loading dataset from: {data_path}")

# ✅ Load your base dataset
df = pd.read_csv(data_path)

# Function to generate enhanced data
def enhance_dataset(df, multiplier=5):
    new_data = []

    for i in range(multiplier * len(df)):
        base = df.iloc[i % len(df)]
        review = base['review']
        label = base['label']

        # Random fake username
        username = fake.user_name()

        # Random date (past 2 years)
        date = fake.date_between(start_date='-2y', end_date='today')

        # Star rating (based on label)
        if label == 'real':
            rating = random.choice([4, 5])
        else:
            rating = random.choice([1, 2])

        new_data.append({
            'username': username,
            'date': date,
            'rating': rating,
            'review': review,
            'label': label
        })

    return pd.DataFrame(new_data)

# ✅ Generate enhanced dataset
enhanced_df = enhance_dataset(df, multiplier=5)

# ✅ Save enhanced data
enhanced_df.to_csv(output_path, index=False)

print(f"\n✅ Enhanced dataset created successfully with {len(enhanced_df)} reviews")
print(f"📁 Saved to: {output_path}")
print("\n🧾 Preview of new dataset:\n")
print(enhanced_df.head(5))
