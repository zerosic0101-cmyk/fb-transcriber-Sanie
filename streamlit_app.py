import streamlit as st
import yt_dlp
import whisper
import os

st.title("📹 Facebook Video Transcriber")
st.write("Paste a public Facebook video link to get the transcript.")

url = st.text_input("Facebook Video URL", placeholder="https://www.facebook.com/...")

if st.button("Get Transcript"):
    if url:
        try:
            with st.spinner("Downloading audio and transcribing... this may take a moment."):
                # Download audio using yt-dlp
                ydl_opts = {
                    'format': 'm4a/bestaudio/best',
                    'outtmpl': 'audio.m4a',
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Transcribe with Whisper (using 'base' model for speed)
                model = whisper.load_model("base")
                result = model.transcribe("audio.m4a")
                
                st.success("Done!")
                st.text_area("Your Transcript:", value=result["text"], height=300)
                st.download_button("Download Transcript", result["text"], file_name="transcript.txt")
                
                # Cleanup local file
                if os.path.exists("audio.m4a"):
                    os.remove("audio.m4a")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a URL first.")
