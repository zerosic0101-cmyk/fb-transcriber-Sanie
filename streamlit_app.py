import streamlit as st
import yt_dlp
import whisper
import os
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Money Printer Gang Transcriber", page_icon="💰", layout="centered")

# 2. CSS for Minimalist Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stTextInput>div>div>input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; border-radius: 8px !important; padding: 15px !important; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00C853 0%, #B2FF59 100%); color: black; border: none; border-radius: 12px; padding: 15px; font-weight: 700; letter-spacing: 1px; transition: 0.3s; margin-top: 10px; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0, 200, 83, 0.4); }
    .stTextArea>div>div>textarea { background-color: #161b22 !important; color: #b0b0b0 !important; border: 1px solid #30363d !important; border-radius: 8px !important; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 style='text-align: center; color: #00C853; margin-bottom: 0;'>Money Printer Gang</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Official Video-to-Text Transcriber</p>", unsafe_allow_html=True)
st.write("---")

# 4. Main Logic
url = st.text_input("", placeholder="Paste video link here...")

if st.button("RUN TRANSCRIPTION"):
    if url:
        try:
            with st.status("Processing...", expanded=True) as status:
                st.write("🐂 Ginagatasan na...")
                ydl_opts = {'format': 'm4a/bestaudio/best', 'outtmpl': 'audio.m4a', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.write("🧠 Malapit na wait lang...")
                model = whisper.load_model("base")
                result = model.transcribe("audio.m4a")
                
                # Extract text correctly from dictionary
                final_text = str(result.get("text", "")).strip()
                status.update(label="Complete!", state="complete", expanded=False)

            if final_text:
                st.subheader("Transcript")
                st.text_area("", value=final_text, height=250, key="transcript_box")
                
                # 5. JavaScript Copy Button
                copy_code = f"""
                <button onclick="copyToClipboard()" style="width: 100%; background-color: #21262d; color: white; border: 1px solid #30363d; border-radius: 8px; padding: 10px; cursor: pointer; font-family: sans-serif; font-weight: 600;">
                    📋 Copy Text
                </button>
                <script>
                function copyToClipboard() {{
                    const text = `{final_text.replace('`', "'")}`;
                    navigator.clipboard.writeText(text).then(() => {{
                        alert("Copied to clipboard!");
                    }});
                }}
                </script>
                """
                components.html(copy_code, height=50)
            
            if os.path.exists("audio.m4a"):
                os.remove("audio.m4a")
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Waiting for link...")

# Footer (No link, just minimal text)
st.markdown("<p style='text-align: center; color: #30363d; font-size: 0.7rem; margin-top: 50px;'>MPG Tool v1.0</p>", unsafe_allow_html=True)
