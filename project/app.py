import streamlit as st
import requests
import os
import pandas as pd

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/analyze"

st.title("📊 News Sentiment Analysis & TTS in Hindi")

# Input field for company name
company_name = st.text_input("Enter Company Name", "")

if st.button("Analyze"):
    if not company_name:
        st.warning("⚠️ Please enter a company name.")
    else:
        st.info(f"Analyzing news for {company_name}...")

        response = requests.post(
            BACKEND_URL,
            json={"company_name": company_name}
        )

        if response.status_code == 200:
            data = response.json()

            st.success("✅ Analysis Complete!")

            # ✅ Display Sentiment Summary
            st.subheader("📊 Sentiment Summary")
            st.json(data["sentiment_summary"])

            # ✅ Display Articles
            st.subheader("📰 Extracted Articles")
            
            df = pd.DataFrame(data["articles"])
            for _, article in df.iterrows():
                st.markdown(f"### [{article['title']}]({article['url']})")
                st.write(f"**Summary:** {article['summary']}")
                st.write("---")

            # ✅ Display Hindi TTS Audio
            st.subheader("🔊 Hindi TTS Audio Output")

            audio_file = data.get("audio_file")

            if audio_file and os.path.exists(audio_file):
                # Display download button and audio player
                with open(audio_file, "rb") as audio:
                    st.download_button(
                        label="🔊 Download Hindi TTS Audio",
                        data=audio,
                        file_name=f"{company_name}_tts_hindi.mp3",
                        mime="audio/mpeg"
                    )
                st.audio(audio_file, format="audio/mp3")
                st.success("✅ Hindi TTS audio displayed successfully!")
            else:
                st.error("❌ TTS file not found.")

        else:
            st.error("❌ Error analyzing news. Please try again.")
