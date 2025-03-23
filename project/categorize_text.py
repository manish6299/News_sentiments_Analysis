import pandas as pd
from nltk.corpus import stopwords


# Preprocessing function
def preprocess_text(text):
    """Tokenize and clean the input text"""
    tokens = text.lower().split()

    # Remove punctuation and stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    return tokens


# Function to calculate similarity score between text and bag of words
def similarity_score(text, bow):
    """Calculate similarity score between text and BoW"""
    
    tokens = preprocess_text(text)

    # Ensure the BoW contains the 'Word' and 'Frequency' columns
    if 'Word' not in bow.columns or 'Frequency' not in bow.columns:
        print("Invalid BoW format. Ensure it contains 'Word' and 'Frequency' columns.")
        return 0

    # Calculate similarity score
    common_words = set(tokens) & set(bow['Word'])
    
    # Sum the frequencies of matching words
    score = sum(bow[bow['Word'] == word]['Frequency'].values[0] for word in common_words)

    return score


# Function to classify text domain using bag of words
def classify_text_domain(text):
    """Classify text domain based on similarity score with BoW files"""

    # Load BoW CSV files for different domains
    try:
        reliance_bow = pd.read_csv("reliance_bow.csv")
    except FileNotFoundError:
        print("BoW file not found.")
        return "Unknown"

    # Ensure CSV files are not empty
    if reliance_bow.empty:
        print("BoW file is empty.")
        return "Unknown"

    # Calculate similarity scores
    scores = {
        "Reliance": similarity_score(text, reliance_bow)
    }

    # Determine the domain with the highest similarity score
    domain = max(scores, key=scores.get)

    print(f"Scores: {scores}")  # Display

