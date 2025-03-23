from flask import Flask, request, jsonify
import os
from sentiment_analysis import perform_sentiment_analysis, comparative_analysis
from tts_hindi import generate_hindi_gtts  # Updated to use gTTS
import pandas as pd

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Perform news sentiment analysis and TTS."""
    try:
        company_name = request.json.get('company_name')

        if not company_name:
            return jsonify({"error": "Company name is required"}), 400

        # CSV file with extracted articles
        csv_file = f"company_news/{company_name}_news.csv"

        if not os.path.exists(csv_file):
            return jsonify({"error": f"No data found for {company_name}"}), 404

        # Perform sentiment analysis
        sentiment_df = perform_sentiment_analysis(csv_file)
        sentiment_summary = comparative_analysis(sentiment_df)

        # ✅ Generate Hindi TTS using gTTS
        summary_text = ". ".join(sentiment_df['summary'].tolist())
        audio_file = generate_hindi_gtts(summary_text, company_name)

        # Extract article details
        articles = sentiment_df[['title', 'summary', 'url']].to_dict(orient='records')

        return jsonify({
            "company": company_name,
            "sentiment_summary": sentiment_summary,
            "articles": articles,
            "audio_file": audio_file
        })

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/generate-tts', methods=['POST'])
def generate_tts_api():
    """Generate TTS API endpoint using gTTS."""
    try:
        data = request.get_json()
        text = data.get('text')
        company_name = data.get('company_name', 'default_company')

        if not text:
            return jsonify({"error": "Text is required"}), 400

        audio_file = generate_hindi_gtts(text, company_name)

        if audio_file and os.path.exists(audio_file):
            return jsonify({
                "message": "✅ TTS generated successfully",
                "audio_file": audio_file
            })
        else:
            return jsonify({"error": "Failed to generate TTS"}), 500

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
