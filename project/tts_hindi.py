from gtts import gTTS
import os


def generate_hindi_gtts(text, company_name):
    """
    Generate Hindi TTS using gTTS.
    """
    try:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        audio_file = os.path.join(output_dir, f"{company_name}_tts_hindi.mp3")

        # ✅ Generate Hindi TTS
        tts = gTTS(text=text, lang="hi")
        tts.save(audio_file)

        print(f"✅ Hindi TTS saved: {audio_file}")
        return audio_file

    except Exception as e:
        print(f"❌ Error generating Hindi TTS with gTTS: {e}")
        return None
