# src/app_v2.py
from flask import Flask, request, jsonify, render_template
import joblib
import os
from src.preprocessing import clean_text
from src.scrape_amazon import scrape_amazon_reviews  # import the scraper
import numpy as np
import sklearn
print("✅ sklearn version on server:", sklearn.__version__)

app = Flask(__name__, template_folder='../frontend')

# ✅ Load trained model safely
model_path = os.path.join(os.path.dirname(__file__), '../models/fake_review_model.pkl')
model_path = os.path.normpath(model_path)

try:
    model = joblib.load(model_path)
    print(f"✅ Model loaded successfully from: {model_path}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None


# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    """Serve main frontend page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Predict authenticity of manually entered review"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.form.get('review', '')
    if not data.strip():
        return jsonify({'error': 'Please enter a review!'}), 400

    clean_review = clean_text(data)
    prediction = model.predict([clean_review])[0]

    # LinearSVC doesn’t have predict_proba → approximate confidence
    if hasattr(model, "decision_function"):
        decision = model.decision_function([clean_review])[0]
        confidence = 1 / (1 + np.exp(-abs(decision))) * 100
    else:
        confidence = 60.0  # fallback confidence

    return jsonify({
        'prediction': prediction,
        'confidence': f"{confidence:.2f}%"
    })


@app.route('/analyze_url', methods=['POST'])
def analyze_url():
    """Scrape Amazon product reviews and analyze them with the model"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    print(f"🔗 Analyzing product URL: {url}")
    reviews = scrape_amazon_reviews(url, max_pages=10)

    if not reviews:
        print("⚠️ No reviews found or scraping blocked.")
        return jsonify({'error': 'No reviews found or scraping blocked'}), 400

    # Clean and predict all reviews
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


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
