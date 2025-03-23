# import nltk
# nltk.download('all')
from gtts import gTTS

# Sample Hindi text
text = "नमस्ते, यह एक परीक्षण संदेश है।"

# Generate TTS in Hindi
tts = gTTS(text=text, lang='hi')
tts.save("test_hindi.mp3")

print("✅ Hindi TTS audio saved successfully!")
