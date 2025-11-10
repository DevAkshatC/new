# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import os
from preprocessing import clean_text

app = Flask(__name__, template_folder='../frontend')

# ✅ Safe model loading
model_path = os.path.join(os.path.dirname(__file__), '../models/fake_review_model.pkl')
model_path = os.path.normpath(model_path)

# ✅ Load model safely
try:
    model = joblib.load(model_path)
    print(f"✅ Model loaded successfully from: {model_path}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'})

    data = request.form.get('review', '')
    if not data.strip():
        return jsonify({'prediction': 'Please enter a review!'})

    clean_review = clean_text(data)

    # ✅ Get both prediction and probability
    probabilities = model.predict_proba([clean_review])[0]
    prediction = model.classes_[probabilities.argmax()]
    confidence = round(probabilities.max() * 100, 2)

    return jsonify({
        'prediction': prediction,
        'confidence': f"{confidence}%"
    })


if __name__ == '__main__':
    app.run(debug=True)
