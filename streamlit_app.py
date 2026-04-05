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
    .stTextArea>div>div>textarea { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; border-radius: 8px !important; font-size: 15px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 style='text-align: center; color: #00C853; margin-bottom: 0;'>Money Printer Gang</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>High-Accuracy AI Transcriber</p>", unsafe_allow_html=True)
st.write("---")

# 4. Main Logic
url = st.text_input("", placeholder="Paste video link here...")

if st.button("RUN TRANSCRIPTION"):
    if url:
        try:
            with st.status("Processing High-Accuracy Script...", expanded=True) as status:
                st.write("📥 Downloading best audio quality...")
                ydl_opts = {
                    'format': 'm4a/bestaudio/best',
                    'outtmpl': 'audio.m4a',
                    'quiet': True,
                    'no_warnings': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.write("🧠 AI is analyzing speech (Model: Small)...")
                # Using 'small' model for significantly better accuracy
                model = whisper.load_model("small")
                
                # Added fp16=False to prevent errors on CPU-only servers
                # Added verbose=False to keep logs clean
                result = model.transcribe("audio.m4a", fp16=False)
                
                final_text = str(result.get("text", "")).strip()
                status.update(label="Transcription Finished!", state="complete", expanded=False)

            if final_text:
                st.subheader("Final Script")
                st.text_area("", value=final_text, height=350, key="transcript_box")
                
                # 5. Modern Copy Button
                # We use a clean string for the JS to avoid breaking on quotes
                js_text = final_text.replace('"', '\\"').replace("'", "\\'").replace("\n", "\\n")
                copy_code = f"""
                <button onclick="copyToClipboard()" style="width: 100%; background-color: #21262d; color: #00C853; border: 1px solid #30363d; border-radius: 12px; padding: 12px; cursor: pointer; font-family: sans-serif; font-weight: 700; font-size: 16px;">
                    📋 COPY SCRIPT
                </button>
                <script>
                function copyToClipboard() {{
                    const text = "{js_text}";
                    const el = document.createElement('textarea');
                    el.value = text;
                    document.body.appendChild(el);
                    el.select();
                    document.execCommand('copy');
                    document.body.removeChild(el);
                    alert("Script copied to clipboard!");
                }}
                </script>
                """
                components.html(copy_code, height=60)
            
            # Auto-cleanup to save server space
            if os.path.exists("audio.m4a"):
                os.remove("audio.m4a")
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please enter a link to begin.")

# Minimalist Footer
st.markdown("<p style='text-align: center; color: #30363d; font-size: 0.7rem; margin-top: 50px;'>MPG Tool v2.0 • High Accuracy Mode</p>", unsafe_allow_html=True)
