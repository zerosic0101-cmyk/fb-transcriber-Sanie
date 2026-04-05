import streamlit as st
import yt_dlp
import whisper
import os
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Sanie Transcribe", page_icon="🌙", layout="centered")

# 2. CSS for Minimalist Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stTextInput>div>div>input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; border-radius: 8px !important; padding: 15px !important; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #5865F2 0%, #8000FF 100%); color: white; border: none; border-radius: 12px; padding: 15px; font-weight: 600; letter-spacing: 1px; transition: 0.3s; margin-top: 10px; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(88, 101, 242, 0.4); }
    .stTextArea>div>div>textarea { background-color: #161b22 !important; color: #b0b0b0 !important; border: 1px solid #30363d !important; border-radius: 8px !important; font-size: 14px; }
    .footer { position: fixed; left: 0; bottom: 20px; width: 100%; text-align: center; color: #8b949e; font-size: 0.8rem; }
    .footer a { color: #5865F2; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 0;'>Sanie Transcribe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>AI-Powered Link to Text</p>", unsafe_allow_html=True)
st.write("---")

# 4. Main Logic
url = st.text_input("", placeholder="Paste Facebook link here...")

if st.button("RUN TRANSCRIPTION"):
    if url:
        try:
            with st.status("Processing...", expanded=True) as status:
                st.write("📥 Downloading...")
                ydl_opts = {'format': 'm4a/bestaudio/best', 'outtmpl': 'audio.m4a', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.write("🧠 Transcribing...")
                model = whisper.load_model("base")
                
                # THE FIX IS HERE:
                result = model.transcribe("audio.m4a")
                final_text = str(result.get("text", "")).strip() 
                
                status.update(label="Complete!", state="complete", expanded=False)

            if final_text:
                st.subheader("Transcript")
                st.text_area("", value=final_text, height=250, key="transcript_box")
                
                # 5. JavaScript Copy Button
                copy_code = f"""
                <button onclick="copyToClipboard()" style="width: 100%; background-color: #21262d; color: white; border: 1px solid #30363d; border-radius: 8px; padding: 10px; cursor: pointer; font-family: sans-serif;">
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

# 6. TikTok Footer
st.markdown(f"""
    <div class="footer">
        Created by <a href="https://tiktok.com" target="_blank">@sah_niee on TikTok</a>
    </div>
    """, unsafe_allow_html=True)
