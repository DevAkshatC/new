# src/app_v2.py

from flask import Flask, request, jsonify, render_template
import joblib
import os
<<<<<<< HEAD
import numpy as np
import nltk
from preprocessing import clean_text
from scrape_amazon import scrape_amazon_reviews

# 🔹 Download required nltk data (important for Render)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 🔹 Correct frontend folder path for Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, template_folder=FRONTEND_DIR)

# 🔹 Safe model loading
model_path = os.path.join(BASE_DIR, "..", "models", "fake_review_model.pkl")
=======
from src.preprocessing import clean_text
from src.scrape_amazon import scrape_amazon_reviews
import numpy as np
import sklearn

print("✅ sklearn version on server:", sklearn._version_)

app = Flask(_name_, template_folder='../frontend')

# Load model
model_path = os.path.join(os.path.dirname(_file_), '../models/fake_review_model.pkl')
>>>>>>> 1017ad95a2515daa3303379c12cb5e1ef6674705
model_path = os.path.normpath(model_path)

try:
    model = joblib.load(model_path)
    print(f"✅ Model loaded successfully from: {model_path}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None


# Temporary test endpoint — remove after debugging
@app.route('/_scrape_test')
def scrape_test():
    test_url = "https://www.amazon.in/dp/B0B3CP96J9"
    reviews = scrape_amazon_reviews(test_url, max_pages=10)
    return {
        "ok": True,
        "sample_count": len(reviews),
        "samples": reviews[:50]
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.form.get('review', '')
    if not data.strip():
        return jsonify({'error': 'Please enter a review!'}), 400

    clean_review = clean_text(data)
    prediction = model.predict([clean_review])[0]

<<<<<<< HEAD
    # If model supports probability
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([clean_review])[0]
        confidence = probabilities.max() * 100
    elif hasattr(model, "decision_function"):
=======
    if hasattr(model, "decision_function"):
>>>>>>> 1017ad95a2515daa3303379c12cb5e1ef6674705
        decision = model.decision_function([clean_review])[0]
        confidence = 1 / (1 + np.exp(-abs(decision))) * 100
    else:
        confidence = 60.0

    return jsonify({
        'prediction': prediction,
        'confidence': f"{confidence:.2f}%"
    })


@app.route('/analyze_url', methods=['POST'])
def analyze_url():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    print(f"🔗 Analyzing product URL: {url}")
    reviews = scrape_amazon_reviews(url, max_pages=5)

    if not reviews:
 
        return jsonify({'error': 'No reviews found or scraping blocked'}), 400

    cleaned = [clean_text(r) for r in reviews]
    preds = model.predict(cleaned)

    total = len(preds)
    fake_count = (preds == "fake").sum()
    real_count = (preds == "real").sum()

    result = {
        "total_reviews": total,
        "fake_count": int(fake_count),
        "real_count": int(real_count),
        "fake_percent": round((fake_count / total) * 100, 2),
        "real_percent": round((real_count / total) * 100, 2),
        "samples": [
            {"review": r, "prediction": p}
            for r, p in zip(reviews[:10], preds[:10])
        ],
    }

    print(f"✅ Analysis Complete → Total: {total}, Fake: {fake_count}, Real: {real_count}")
    return jsonify(result)


<<<<<<< HEAD
# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

=======
if _name_ == '_main_':
    app.run(debug=True)
>>>>>>> 1017ad95a2515daa3303379c12cb5e1ef6674705
