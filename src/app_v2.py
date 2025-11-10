# src/app_v2.py
from flask import Flask, request, jsonify, render_template
import joblib
import os
from src.preprocessing import clean_text
from src.scrape_amazon import scrape_amazon_reviews
import numpy as np
import sklearn

print("✅ sklearn version on server:", sklearn.__version__)

app = Flask(__name__, template_folder='../frontend')

# Load model
model_path = os.path.join(os.path.dirname(_file_), '../models/fake_review_model.pkl')
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
    # replace this example with any Amazon product URL you want to test
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
    """Predict authenticity of manually entered review"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.form.get('review', '')
    if not data.strip():
        return jsonify({'error': 'Please enter a review!'}), 400

    clean_review = clean_text(data)
    prediction = model.predict([clean_review])[0]

    if hasattr(model, "decision_function"):
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
    """Scrape Amazon product reviews and analyze them with the model"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    print(f"🔗 Analyzing product URL: {url}")
    reviews = scrape_amazon_reviews(url, max_pages=10)

    if not reviews:
        print("⚠ No reviews found or scraping blocked.")
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


if _name_ == '_main_':
    app.run(debug=True)
