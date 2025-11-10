import pandas as pd
import joblib
import os
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from preprocessing import clean_text

# ===============================================
# 📂 PATH SETUP
# ===============================================
base_path = os.path.dirname(os.path.dirname(__file__))  # goes one level up from src/
data_path = os.path.join(base_path, 'data', 'reviews_large_enhanced.csv')
model_path = os.path.join(base_path, 'models', 'fake_review_model.pkl')

print(f"📂 Loading dataset from: {data_path}")

# ===============================================
# 📄 LOAD DATASET
# ===============================================
df = pd.read_csv(data_path)
print(f"✅ Loaded dataset with {len(df)} reviews\n")
print(df['label'].value_counts(), "\n")

print("📊 Dataset Balance (%):")
print(df['label'].value_counts(normalize=True) * 100)

# Drop null values
df = df.dropna(subset=['review', 'label'])

# ===============================================
# 🧹 TEXT CLEANING
# ===============================================
print("\n🧹 Cleaning text and merging metadata...")
df['combined_text'] = (
    df['review'].astype(str)
    + " user:" + df['username'].astype(str)
    + " rating:" + df['rating'].astype(str)
    + " date:" + df['date'].astype(str)
)
df['clean'] = df['combined_text'].apply(clean_text)

# ===============================================
# ✂️ TRAIN / TEST SPLIT
# ===============================================
X_train, X_test, y_train, y_test = train_test_split(
    df['clean'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

# ===============================================
# ⚙️ PIPELINE: TF-IDF + LOGISTIC REGRESSION (CV)
# ===============================================
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 3),
        stop_words='english',
        sublinear_tf=True
    )),
    ('clf', LogisticRegressionCV(
        cv=5,
        max_iter=3000,
        class_weight='balanced',
        solver='liblinear',
        scoring='f1',
        random_state=42
    ))
])

# ===============================================
# 🚀 TRAIN MODEL
# ===============================================
print("\n🚀 Training optimized Logistic RegressionCV model...")
pipeline.fit(X_train, y_train)
print("✅ Training completed successfully!\n")

# ===============================================
# 📊 EVALUATION
# ===============================================
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))
print(f"✅ Accuracy: {acc * 100:.2f}%")

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, df['clean'], df['label'], cv=cv, scoring='f1_macro')
print(f"📈 Cross-Validation F1-Score: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}\n")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("🧩 Confusion Matrix:\n", cm)

# ===============================================
# 💾 SAVE MODEL
# ===============================================
joblib.dump(pipeline, model_path)
print(f"\n✅ Model saved successfully at: {model_path}")

# ===============================================
# 🔍 SAMPLE PREDICTIONS
# ===============================================
sample_reviews = [
    "This product is amazing! Totally worth it.",
    "Worst product ever. Completely fake reviews.",
    "Good quality, fast delivery.",
    "I would not recommend this to anyone.",
    "This is a scam, don’t waste your money.",
    "Great service, very satisfied with the purchase."
]

print("\n--- 🔍 Sample Predictions ---")
for review in sample_reviews:
    clean_review = clean_text(review)
    probabilities = pipeline.predict_proba([clean_review])[0]
    prediction = pipeline.classes_[np.argmax(probabilities)]
    confidence = round(probabilities.max() * 100, 2)
    print(f"📝 Review: {review}")
    print(f"➡️ Prediction: {prediction.upper()} ({confidence}% confidence)\n")
