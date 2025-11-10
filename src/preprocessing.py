# preprocessing.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download NLTK resources (only runs first time on Render)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # ✅ required for new NLTK
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """
    Cleans review text by:
    1. Lowercasing
    2. Removing URLs, numbers, punctuation
    3. Tokenizing words
    4. Removing stopwords
    5. Lemmatizing (run -> run, running -> run)
    """
    if not isinstance(text, str):
        text = str(text)

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+', ' ', text)

    # Keep only letters
    text = re.sub(r'[^a-z\s]', ' ', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]

    return " ".join(tokens)
