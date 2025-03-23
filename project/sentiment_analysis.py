import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    """Perform sentiment analysis on the given text."""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return sentiment, round(polarity, 2)

    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral", 0.0


def perform_sentiment_analysis(csv_file):
    """Analyze sentiment for all articles in the CSV."""
    df = pd.read_csv(csv_file)

    if 'summary' not in df.columns:
        print("No 'summary' column found in CSV.")
        return None

    df['sentiment'], df['polarity'] = zip(*df['summary'].apply(analyze_sentiment))

    # Save the result with sentiment analysis
    output_csv = csv_file.replace('.csv', '_sentiment.csv')
    df.to_csv(output_csv, index=False)
    print(f"✅ Sentiment analysis saved to {output_csv}")

    return df


def comparative_analysis(df):
    """Perform comparative sentiment analysis across multiple articles."""
    sentiment_counts = df['sentiment'].value_counts(normalize=True) * 100

    print("\n📊 Sentiment Distribution:")
    print(sentiment_counts)

    summary = {
        "positive": sentiment_counts.get("Positive", 0),
        "negative": sentiment_counts.get("Negative", 0),
        "neutral": sentiment_counts.get("Neutral", 0)
    }

    return summary
