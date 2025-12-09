import streamlit as st
import numpy as np
import cv2
from PIL import Image
from ocr_backend import extract_text, extract_text_from_pdf  # Importing OCR functions from backend
from deep_translator import GoogleTranslator
import speech_recognition as sr
import tempfile
import os
from moviepy.editor import VideoFileClip
import re
import requests
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="AI Text Extraction & Translation",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better design
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Global text styling - more specific */
    p, span, label, div:not(.stSelectbox):not(.stTextArea) {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        margin: 2rem auto;
    }
    
    /* Title styling */
    h1 {
        color: #000000 !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: none;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #000000 !important;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 700 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e0e5ec 0%, #ffffff 100%);
        border-right: 3px solid #cccccc;
    }
    
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar selectbox text */
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stSelectbox div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #e8e8e8;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 700;
        color: #000000 !important;
        border: 2px solid #cccccc;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #000000 !important;
        border: 3px solid #000000;
        font-weight: 900 !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: #e8e8e8;
        color: #000000 !important;
        border: 3px solid #000000;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 900 !important;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: #ffffff;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: #d4d4d4;
        color: #000000 !important;
        border: 3px solid #000000;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 900 !important;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        background: #ffffff;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 3px solid #000000;
        font-size: 1.1rem;
        padding: 1rem;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        line-height: 1.6;
    }
    
    /* Ensure textarea text is always visible */
    textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Selectbox styling */
    .stSelectbox select,
    .stSelectbox div[data-baseweb="select"] > div {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox option {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 2rem;
        border: 3px dashed #000000;
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] span {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Camera input */
    [data-testid="stCameraInput"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 2rem;
        border: 3px dashed #000000;
    }
    
    [data-testid="stCameraInput"] label,
    [data-testid="stCameraInput"] span {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        font-weight: 700 !important;
        background-color: #f0f0f0 !important;
        border: 2px solid #000000 !important;
    }
    
    .stSuccess *, .stInfo * {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #000000 !important;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #000000 !important;
        font-weight: 900 !important;
        margin-top: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        border: 3px solid #000000;
        color: #000000 !important;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 900 !important;
        margin-bottom: 0.5rem;
        color: #000000 !important;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("# 📷 AI Text Extraction & Translation")
st.markdown('<p class="subtitle">🚀 Extract text from images & PDFs, then translate to 15+ languages instantly</p>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <div class="feature-title">Multi-Source Input</div>
            <div class="feature-desc">Camera, Images & PDFs</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">15 Languages</div>
            <div class="feature-desc">OCR in Multiple Languages</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎤</div>
            <div class="feature-title">Voice to Text</div>
            <div class="feature-desc">Speech Recognition</div>
        </div>
    """, unsafe_allow_html=True)

# Additional feature row
col4, col5 = st.columns(2)
with col4:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Smart Translation</div>
            <div class="feature-desc">Auto-detect & Translate</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎬</div>
            <div class="feature-title">Video to Text</div>
            <div class="feature-desc">Extract & Convert Audio</div>
        </div>
    """, unsafe_allow_html=True)

# Third feature row
col6, col7 = st.columns(2)
with col6:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💾</div>
            <div class="feature-title">Export to TXT</div>
            <div class="feature-desc">Download All Results</div>
        </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Quick & Accurate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar styling
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings Panel")
st.sidebar.markdown("---")

# Language selection
st.sidebar.markdown("### 🌐 OCR Language")
languages = {
    "English": "eng",
    "Spanish": "spa",
    "French": "fra",
    "German": "deu",
    "Italian": "ita",
    "Portuguese": "por",
    "Russian": "rus",
    "Chinese (Simplified)": "chi_sim",
    "Japanese": "jpn",
    "Korean": "kor",
    "Arabic": "ara",
    "Hindi": "hin",
    "Bengali": "ben",
    "Turkish": "tur",
    "Dutch": "nld"
}

# Translation language codes (for Google Translate)
translation_languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Turkish": "tr",
    "Dutch": "nl"
}

selected_language = st.sidebar.selectbox(
    "Choose language for text extraction:",
    options=list(languages.keys()),
    index=0,
    help="Select the language of the text in your image/PDF"
)
lang_code = languages[selected_language]

st.sidebar.markdown("---")

# Translation settings
st.sidebar.markdown("### 🔤 Translation Options")
enable_translation = st.sidebar.checkbox("🔄 Enable Translation", value=False)
if enable_translation:
    target_language = st.sidebar.selectbox(
        "Translate extracted text to:",
        options=list(translation_languages.keys()),
        index=0,
        help="Automatically translate the extracted text"
    )
    target_lang_code = translation_languages[target_language]

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.info("🎯 **15 Languages Supported**\n\n✅ OCR Accuracy: High\n\n⚡ Fast Processing")
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.success("📌 Use clear, well-lit images\n\n📌 Higher resolution = better OCR\n\n📌 PDF text extraction is instant")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Language Data")
with st.sidebar.expander("Download Additional Languages"):
    st.markdown("""
    **English** is pre-installed. For other languages:
    
    Select a language below to download:
    """)
    
    # Language download helper
    lang_files = {
        "Hindi": "hin",
        "Spanish": "spa",
        "French": "fra",
        "German": "deu",
        "Arabic": "ara",
        "Chinese (Simplified)": "chi_sim",
        "Russian": "rus",
        "Japanese": "jpn",
        "Korean": "kor"
    }
    
    selected_download = st.selectbox("Select language to download:", ["-- Select --"] + list(lang_files.keys()), key="lang_download")
    
    if selected_download != "-- Select --":
        if st.button(f"📥 Download {selected_download}", key="download_lang_btn"):
            lang_code = lang_files[selected_download]
            url = f"https://github.com/tesseract-ocr/tessdata/raw/main/{lang_code}.traineddata"
            tessdata_path = Path(r"C:\Program Files\Tesseract-OCR\tessdata")
            
            try:
                with st.spinner(f"Downloading {selected_download} language data..."):
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    
                    # Save to tessdata folder
                    file_path = tessdata_path / f"{lang_code}.traineddata"
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    st.success(f"✅ {selected_download} language downloaded successfully!")
                    st.info("Please restart the app to use the new language.")
            except PermissionError:
                st.error("❌ Permission denied. Please run as Administrator or manually download to tessdata folder.")
            except Exception as e:
                st.error(f"❌ Download failed: {str(e)}")
                st.info(f"Manual download: [Click here]({url})")
    
    st.markdown("---")
    st.caption("💡 If auto-download fails, download manually from GitHub and place in tessdata folder.")


# Tabs for different input methods
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📷 Camera Capture", "🖼️ Upload Image", "📄 Upload PDF", "🎤 Voice to Text", "🎬 Video to Text"])

with tab1:
    st.markdown("### 📸 Capture Image with Camera")
    st.info("💡 Click the camera button below to take a picture")
    # Camera Input for live capture
    captured_image = st.camera_input("📷 Activate Camera")

with tab2:
    st.markdown("### 🖼️ Upload an Image File")
    st.info("💡 Supported formats: JPG, PNG, JPEG")
    # File Uploader for manual image upload
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"], help="Drag and drop or click to browse")

with tab3:
    st.markdown("### 📄 Upload a PDF Document")
    st.info("💡 Extract text from multi-page PDFs instantly")
    # File Uploader for PDF
    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"], help="Drag and drop or click to browse")

# Process Image (either from camera or uploaded file)
if captured_image or uploaded_file:
    # Load the image
    if captured_image:
        image = Image.open(captured_image)
    else:
        image = Image.open(uploaded_file)

    col_img, col_space = st.columns([2, 1])
    with col_img:
        st.image(image, caption="📷 Captured Image", use_container_width=True)

    # Save image temporarily for OCR processing
    image_np = np.array(image)
    image_path = "temp_image.jpg"
    cv2.imwrite(image_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

    # Extract text using OCR
    with st.spinner(f"🔍 Extracting text from image ({selected_language})..."):
        try:
            extracted_text = extract_text(image_path, lang=lang_code)
        except Exception as e:
            if "traineddata" in str(e):
                st.error(f"❌ Language data file not found for {selected_language}!")
                st.info(f"""
                📥 **Download Required Language Data:**
                
                1. Visit: https://github.com/tesseract-ocr/tessdata
                2. Download `{lang_code}.traineddata`
                3. Place it in: `C:\\Program Files\\Tesseract-OCR\\tessdata\\`
                4. Restart the app
                
                Or try using **English** language which is already installed.
                """)
                st.stop()
            else:
                st.error(f"❌ Error extracting text: {str(e)}")
                st.stop()
        
        extracted_text = extracted_text if extracted_text else ""
    
    st.success("✅ Text extraction completed!")
    
    # Check if text contains code
    code_indicators = ['def ', 'class ', 'import ', 'function ', 'var ', 'const ', 'let ', '<?php', '#!/', '{', '}', '()', '=>', 'public ', 'private ', 'return']
    contains_code = any(indicator in extracted_text for indicator in code_indicators)
    
    # Display options
    display_option = st.radio(
        "Display as:",
        ["📝 Plain Text", "💻 Code Format"] if contains_code else ["📝 Plain Text"],
        horizontal=True,
        key="img_display_option"
    )
    
    if display_option == "💻 Code Format":
        st.markdown("### 💻 Extracted Code")
        st.code(extracted_text, language=None, line_numbers=True)
    else:
        st.markdown("### 📝 Extracted Text")
        st.text_area("Text Output", extracted_text, height=300, label_visibility="collapsed")
    
    # Translation
    if enable_translation and extracted_text.strip():
        with st.spinner(f"🔄 Translating to {target_language}..."):
            try:
                translator = GoogleTranslator(source='auto', target=target_lang_code)
                translated_text = translator.translate(extracted_text)
                st.success(f"✅ Translation to {target_language} completed!")
                st.markdown(f"### 🔤 Translated Text ({target_language})")
                st.text_area("Translated Output", translated_text, height=300, label_visibility="collapsed")
                
                # Download button for translated text
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label=f"📥 Download Translated Text ({target_language})",
                        data=translated_text,
                        file_name=f"translated_text_{target_lang_code}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ Translation error: {str(e)}")
    
    # Download button for extracted text
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain",
            use_container_width=True
        )

# Process PDF
if uploaded_pdf:
    st.success(f"✅ PDF uploaded: **{uploaded_pdf.name}**")
    
    # Extract text from PDF
    with st.spinner(f"🔍 Extracting text from PDF ({selected_language})..."):
        try:
            extracted_text = extract_text_from_pdf(uploaded_pdf, lang=lang_code)
        except Exception as e:
            if "traineddata" in str(e):
                st.error(f"❌ Language data file not found for {selected_language}!")
                st.info(f"""
                📥 **Download Required Language Data:**
                
                1. Visit: https://github.com/tesseract-ocr/tessdata
                2. Download `{lang_code}.traineddata`
                3. Place it in: `C:\\Program Files\\Tesseract-OCR\\tessdata\\`
                4. Restart the app
                
                Or try using **English** language which is already installed.
                """)
                st.stop()
        
        try:
            extracted_text = extract_text_from_pdf(uploaded_pdf, lang=lang_code)
            
            st.success("✅ Text extraction completed!")
            
            # Check if text contains code
            code_indicators = ['def ', 'class ', 'import ', 'function ', 'var ', 'const ', 'let ', '<?php', '#!/', '{', '}', '()', '=>', 'public ', 'private ', 'return']
            contains_code = any(indicator in extracted_text for indicator in code_indicators)
            
            # Display options
            display_option = st.radio(
                "Display as:",
                ["📝 Plain Text", "💻 Code Format"] if contains_code else ["📝 Plain Text"],
                horizontal=True,
                key="pdf_display_option"
            )
            
            if display_option == "💻 Code Format":
                st.markdown("### 💻 Extracted Code")
                st.code(extracted_text, language=None, line_numbers=True)
            else:
                st.markdown("### 📝 Extracted Text")
                st.text_area("Text Output", extracted_text, height=300, label_visibility="collapsed")
            
            # Translation
            if enable_translation and extracted_text.strip():
                with st.spinner(f"🔄 Translating to {target_language}..."):
                    try:
                        translator = GoogleTranslator(source='auto', target=target_lang_code)
                        translated_text = translator.translate(extracted_text)
                        st.success(f"✅ Translation to {target_language} completed!")
                        st.markdown(f"### 🔤 Translated Text ({target_language})")
                        st.text_area("Translated Output", translated_text, height=300, label_visibility="collapsed")
                        
                        # Download button for translated text
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label=f"📥 Download Translated Text ({target_language})",
                                data=translated_text,
                                file_name=f"translated_pdf_text_{target_lang_code}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"❌ Translation error: {str(e)}")
            
            # Download button for extracted text
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Extracted Text",
                    data=extracted_text,
                    file_name="extracted_pdf_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"❌ Error extracting text from PDF: {str(e)}")

# Voice to Text Tab
with tab4:
    st.markdown("### 🎤 Voice to Text Conversion")
    st.info("💡 Upload an audio file or record live from your microphone")
    
    # Two columns for options
    voice_option = st.radio(
        "Choose input method:",
        ["📁 Upload Audio File", "🎙️ Record from Microphone"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if voice_option == "📁 Upload Audio File":
        # Audio file uploader
        audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a", "flac", "ogg"], help="Upload audio file for speech recognition")
    
    # Language selection for speech recognition
    speech_languages = {
        "English": "en-US",
        "Spanish": "es-ES",
        "French": "fr-FR",
        "German": "de-DE",
        "Italian": "it-IT",
        "Portuguese": "pt-PT",
        "Russian": "ru-RU",
        "Chinese (Simplified)": "zh-CN",
        "Japanese": "ja-JP",
        "Korean": "ko-KR",
        "Arabic": "ar-SA",
        "Hindi": "hi-IN",
        "Bengali": "bn-IN",
        "Turkish": "tr-TR",
        "Dutch": "nl-NL"
    }
    
    selected_speech_lang = st.selectbox(
        "Select audio language",
        options=list(speech_languages.keys()),
        index=0,
        help="Choose the language spoken in the audio",
        key="upload_audio_lang"
    )
    speech_lang_code = speech_languages[selected_speech_lang]
    
    if voice_option == "📁 Upload Audio File" and audio_file is not None:
        st.success(f"✅ Audio file uploaded: **{audio_file.name}**")
        
        # Display audio player
        st.audio(audio_file, format=f'audio/{audio_file.name.split(".")[-1]}')
        
        # Convert button
        if st.button("🎙️ Convert Speech to Text", use_container_width=True):
            with st.spinner(f"🔍 Converting speech to text ({selected_speech_lang})..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(audio_file.read())
                        tmp_audio_path = tmp_file.name
                    
                    # Initialize recognizer
                    recognizer = sr.Recognizer()
                    
                    # Convert audio to text
                    with sr.AudioFile(tmp_audio_path) as source:
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data, language=speech_lang_code)
                    
                    # Clean up temp file
                    os.unlink(tmp_audio_path)
                    
                    st.success("✅ Speech to text conversion completed!")
                    st.markdown("### 📝 Converted Text")
                    st.text_area("Text Output", text, height=300, label_visibility="collapsed")
                    
                    # Translation option for voice text
                    if enable_translation and text.strip():
                        with st.spinner(f"🔄 Translating to {target_language}..."):
                            try:
                                translator = GoogleTranslator(source='auto', target=target_lang_code)
                                translated_text = translator.translate(text)
                                st.success(f"✅ Translation to {target_language} completed!")
                                st.markdown(f"### 🔤 Translated Text ({target_language})")
                                st.text_area("Translated Output", translated_text, height=300, label_visibility="collapsed")
                                
                                # Download button for translated text
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    st.download_button(
                                        label=f"📥 Download Translated Text ({target_language})",
                                        data=translated_text,
                                        file_name=f"translated_voice_text_{target_lang_code}.txt",
                                        mime="text/plain",
                                        use_container_width=True
                                    )
                            except Exception as e:
                                st.error(f"❌ Translation error: {str(e)}")
                    
                    # Download button for converted text
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download Converted Text",
                            data=text,
                            file_name="voice_to_text.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                except sr.UnknownValueError:
                    st.error("❌ Could not understand the audio. Please try with a clearer recording.")
                except sr.RequestError as e:
                    st.error(f"❌ Could not request results from speech recognition service: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error converting speech to text: {str(e)}")
    
    elif voice_option == "📁 Upload Audio File":
        st.warning("⚠️ Please upload an audio file to begin conversion")
    
    # Microphone recording option
    if voice_option == "🎙️ Record from Microphone":
        st.markdown("### 🎙️ Record from Microphone")
        
        # Language selection for microphone
        mic_speech_lang = st.selectbox(
            "Select language for recording",
            options=list(speech_languages.keys()),
            index=0,
            help="Choose the language you will speak",
            key="mic_audio_lang"
        )
        mic_speech_lang_code = speech_languages[mic_speech_lang]
        
        # Recording duration with custom input option
        col1, col2 = st.columns(2)
        with col1:
            duration_option = st.radio(
                "Recording duration option:",
                ["Use Slider", "Custom Duration"],
                key="duration_option"
            )
        
        if duration_option == "Use Slider":
            duration = st.slider("Recording duration (seconds)", min_value=3, max_value=300, value=10, step=1)
        else:
            duration = st.number_input(
                "Enter custom duration (seconds)",
                min_value=1,
                max_value=3600,
                value=30,
                step=5,
                help="Enter any duration from 1 second to 1 hour (3600 seconds)"
            )
        
        st.info(f"💡 Click the button below and speak into your microphone for {duration} seconds")
        
        # Record button
        if st.button("🎙️ Start Recording", use_container_width=True):
            with st.spinner(f"🔴 Recording for {duration} seconds... Please speak now!"):
                try:
                    # Initialize recognizer
                    recognizer = sr.Recognizer()
                    
                    # Record from microphone
                    with sr.Microphone() as source:
                        st.info("🎤 Adjusting for ambient noise... Please wait...")
                        recognizer.adjust_for_ambient_noise(source, duration=2)
                        
                        # Adjust energy threshold for better recording
                        recognizer.energy_threshold = 4000
                        recognizer.dynamic_energy_threshold = True
                        recognizer.pause_threshold = 0.8  # Seconds of silence before phrase ends
                        
                        st.success(f"✅ Recording started! Speak now for {duration} seconds...")
                        
                        # Record audio for the specified duration
                        audio_data = recognizer.record(source, duration=duration)
                    
                    st.success("✅ Recording completed!")
                    
                    # Convert to text
                    with st.spinner(f"🔍 Converting speech to text ({mic_speech_lang})..."):
                        text = recognizer.recognize_google(audio_data, language=mic_speech_lang_code)
                        
                        st.success("✅ Speech to text conversion completed!")
                        st.markdown("### 📝 Converted Text from Microphone")
                        st.text_area("Text Output", text, height=300, label_visibility="collapsed", key="mic_text_output")
                        
                        # Translation option for microphone text
                        if enable_translation and text.strip():
                            with st.spinner(f"🔄 Translating to {target_language}..."):
                                try:
                                    translator = GoogleTranslator(source='auto', target=target_lang_code)
                                    translated_text = translator.translate(text)
                                    st.success(f"✅ Translation to {target_language} completed!")
                                    st.markdown(f"### 🔤 Translated Text ({target_language})")
                                    st.text_area("Translated Output", translated_text, height=300, label_visibility="collapsed", key="mic_translated_output")
                                    
                                    # Download button for translated text
                                    col1, col2, col3 = st.columns([1, 2, 1])
                                    with col2:
                                        st.download_button(
                                            label=f"📥 Download Translated Text ({target_language})",
                                            data=translated_text,
                                            file_name=f"translated_mic_text_{target_lang_code}.txt",
                                            mime="text/plain",
                                            use_container_width=True,
                                            key="mic_translated_download"
                                        )
                                except Exception as e:
                                    st.error(f"❌ Translation error: {str(e)}")
                        
                        # Download button for converted text
                        st.markdown("---")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="📥 Download Converted Text",
                                data=text,
                                file_name="microphone_to_text.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key="mic_text_download"
                            )
                            
                except sr.WaitTimeoutError:
                    st.error("❌ No speech detected. Please try again and speak clearly into the microphone.")
                except sr.UnknownValueError:
                    st.error("❌ Could not understand the audio. Please try again with clearer speech.")
                except sr.RequestError as e:
                    st.error(f"❌ Could not request results from speech recognition service: {str(e)}")
                except OSError as e:
                    st.error(f"❌ Microphone error: {str(e)}. Please check if your microphone is connected and accessible.")
                except Exception as e:
                    st.error(f"❌ Error recording from microphone: {str(e)}")

# Video to Text Tab
with tab5:
    st.markdown("### 🎬 Video to Text Conversion")
    st.info("💡 Upload a video file to extract audio and convert speech to text")
    
    # Video file uploader
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv", "flv", "wmv"], help="Upload video file to extract audio and convert to text")
    
    # Language selection for video speech recognition
    video_speech_lang = st.selectbox(
        "Select video audio language",
        options=list(speech_languages.keys()),
        index=0,
        help="Choose the language spoken in the video",
        key="video_lang_select"
    )
    video_speech_lang_code = speech_languages[video_speech_lang]
    
    if video_file is not None:
        st.success(f"✅ Video file uploaded: **{video_file.name}**")
        
        # Display video player
        st.video(video_file)
        
        # Convert button
        if st.button("🎬 Extract Audio & Convert to Text", use_container_width=True):
            with st.spinner("🔍 Extracting audio from video..."):
                try:
                    # Save uploaded video temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{video_file.name.split('.')[-1]}") as tmp_video:
                        tmp_video.write(video_file.read())
                        tmp_video_path = tmp_video.name
                    
                    # Extract audio from video
                    st.info("🎵 Extracting audio from video...")
                    video_clip = VideoFileClip(tmp_video_path)
                    
                    # Save audio as WAV
                    tmp_audio_path = tempfile.mktemp(suffix=".wav")
                    video_clip.audio.write_audiofile(tmp_audio_path, codec='pcm_s16le', verbose=False, logger=None)
                    video_clip.close()
                    
                    # Clean up video file
                    os.unlink(tmp_video_path)
                    
                    st.success("✅ Audio extracted successfully!")
                    
                    # Convert audio to text
                    with st.spinner(f"🔍 Converting speech to text ({video_speech_lang})..."):
                        # Initialize recognizer
                        recognizer = sr.Recognizer()
                        
                        # Convert audio to text
                        with sr.AudioFile(tmp_audio_path) as source:
                            audio_data = recognizer.record(source)
                            text = recognizer.recognize_google(audio_data, language=video_speech_lang_code)
                        
                        # Clean up temp audio file
                        os.unlink(tmp_audio_path)
                        
                        st.success("✅ Speech to text conversion completed!")
                        st.markdown("### 📝 Converted Text from Video")
                        st.text_area("Text Output", text, height=300, label_visibility="collapsed", key="video_text_output")
                        
                        # Translation option for video text
                        if enable_translation and text.strip():
                            with st.spinner(f"🔄 Translating to {target_language}..."):
                                try:
                                    translator = GoogleTranslator(source='auto', target=target_lang_code)
                                    translated_text = translator.translate(text)
                                    st.success(f"✅ Translation to {target_language} completed!")
                                    st.markdown(f"### 🔤 Translated Text ({target_language})")
                                    st.text_area("Translated Output", translated_text, height=300, label_visibility="collapsed", key="video_translated_output")
                                    
                                    # Download button for translated text
                                    col1, col2, col3 = st.columns([1, 2, 1])
                                    with col2:
                                        st.download_button(
                                            label=f"📥 Download Translated Text ({target_language})",
                                            data=translated_text,
                                            file_name=f"translated_video_text_{target_lang_code}.txt",
                                            mime="text/plain",
                                            use_container_width=True,
                                            key="video_translated_download"
                                        )
                                except Exception as e:
                                    st.error(f"❌ Translation error: {str(e)}")
                        
                        # Download button for converted text
                        st.markdown("---")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="📥 Download Converted Text",
                                data=text,
                                file_name="video_to_text.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key="video_text_download"
                            )
                            
                except sr.UnknownValueError:
                    st.error("❌ Could not understand the audio from video. Please try with a clearer video.")
                except sr.RequestError as e:
                    st.error(f"❌ Could not request results from speech recognition service: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")
                    # Clean up temp files in case of error
                    try:
                        if 'tmp_video_path' in locals() and os.path.exists(tmp_video_path):
                            os.unlink(tmp_video_path)
                        if 'tmp_audio_path' in locals() and os.path.exists(tmp_audio_path):
                            os.unlink(tmp_audio_path)
                    except:
                        pass
    else:
        st.warning("⚠️ Please upload a video file to begin conversion")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #666;'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>🚀 Powered by Tesseract OCR & Google Translate</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.8;'>
            Built with ❤️ using Streamlit | Support: 15+ Languages | Fast & Accurate
        </p>
        <p style='font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;'>
            © 2025 AI Text Extraction System | All Rights Reserved
        </p>
    </div>
""", unsafe_allow_html=True)
