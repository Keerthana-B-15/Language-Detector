import streamlit as st
import pandas as pd
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
from langcodes import Language

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Function to detect language and translate text
def analyze_text(text):
    try:
        lang_code = detect(text)  # Detect language code
        lang_name = Language.make(language=lang_code).display_name()  # Convert code to full language name
        translation = GoogleTranslator(source=lang_code, target="en").translate(text)
        explanation = f"This text is detected as {lang_name}, which is widely spoken in various regions. It has unique linguistic characteristics and cultural significance."
        return lang_name, translation, explanation
    except:
        return "Unknown", "Translation not available", "Language detection failed."

# Streamlit UI with a modern design
st.set_page_config(page_title="Language Detector", page_icon="🌍", layout="wide")
st.title("🌍 AI-Powered Language Detector")
st.markdown("Detect the language of your text, see its English translation, and get additional insights!")

# Text input area
input_text = st.text_area("Enter your text below:", height=200)

if st.button("Detect Language & Translate"):
    if input_text.strip():
        # Process each line separately
        lines = [line.strip() for line in input_text.split("\n") if line.strip()]
        results = [analyze_text(line) for line in lines]
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(results, columns=["Detected Language", "English Translation", "Explanation"], index=lines)
        st.dataframe(results_df, use_container_width=True)
    else:
        st.warning("Please enter some text to analyze.")
