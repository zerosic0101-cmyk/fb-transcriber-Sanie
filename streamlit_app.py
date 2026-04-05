import streamlit as st
import yt_dlp
import whisper
import os

# Page Config
st.set_page_config(page_title="MPG Transcriber", page_icon="💰")

st.title("💰 Money Printer Gang")
st.caption("AI Video-to-Text")

url = st.text_input("Paste Link Here")

if st.button("RUN"):
    if url:
        try:
            with st.spinner("Processing..."):
                # 1. Download
                ydl_opts = {'format': 'm4a/bestaudio/best', 'outtmpl': 'audio.m4a', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 2. Transcribe
                model = whisper.load_model("base") # Back to base for a quick test
                result = model.transcribe("audio.m4a")
                text = result.strip()
                
                # 3. Display
                st.text_area("Transcript", value=text, height=300)
                st.code(text) # Easy to click and copy
                
                if os.path.exists("audio.m4a"):
                    os.remove("audio.m4a")
        except Exception as e:
            st.error(f"Error: {e}")
