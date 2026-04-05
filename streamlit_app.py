import streamlit as st
import yt_dlp
import whisper
import os

# 1. Page Config & Theme Setup
st.set_page_config(page_title="Sanie Transcribe", page_icon="🌙", layout="centered")

# 2. Modern Dark Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Input Box */
    .stTextInput>div>div>input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }

    /* Modern Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #5865F2 0%, #8000FF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 20px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(88, 101, 242, 0.4);
    }

    /* Results Area */
    .stTextArea>div>div>textarea {
        background-color: #161b22 !important;
        color: #b0b0b0 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Minimalist Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
    }
    .footer a {
        color: #5865F2;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Minimalist Header
st.markdown("<h1 style='text-align: center; color: white;'>Sanie Transcribe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Minimalist AI-Powered Transcription</p>", unsafe_allow_html=True)
st.write("---")

# 4. Main Tool Logic
url = st.text_input("", placeholder="Paste Facebook link here...")

if st.button("TRANSCRIBE"):
    if url:
        try:
            with st.status("Processing...", expanded=True) as status:
                st.write("📥 Fetching audio...")
                ydl_opts = {'format': 'm4a/bestaudio/best', 'outtmpl': 'audio.m4a', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.write("🧠 AI Transcription in progress...")
                model = whisper.load_model("base")
                result = model.transcribe("audio.m4a")
                status.update(label="Complete!", state="complete", expanded=False)

            st.subheader("Result")
            st.text_area("", value=result, height=250)
            
            st.download_button("Download Text File", result, file_name="transcript.txt")
            
            # Clean up
            if os.path.exists("audio.m4a"):
                os.remove("audio.m4a")
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.info("Waiting for a valid URL...")

# 5. Fixed Footer with TikTok Link
st.markdown("""
    <div class="footer">
        Created by <a href="https://www.tiktok.com/@sah_niee?is_from_webapp=1&sender_device=pc" target="_blank">@sah_niee on TikTok</a>
    </div>
    """, unsafe_allow_html=True)
