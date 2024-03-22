import streamlit as st
import os
from googletrans import Translator
from PyPDF2 import PdfReader
from docx import Document

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def translate_file(input_file_path, output_file_paths, target_language):
    # Read text from input file
    if input_file_path.endswith('.docx'):
        doc = Document(input_file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif input_file_path.endswith('.pdf'):
        with open(input_file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
    else:
        raise ValueError("Unsupported file format")

    # Translate text to target language
    translated_text = translate_text(text, target_language)

    # Write translated text to output file
    with open(output_file_paths, 'w', encoding='utf-8') as file:
        file.write(translated_text)

    return output_file_paths

def main():
    st.title("Document Translator")

    # Language selection
    from_language = "English"  # Fixed as English for now
    to_language = st.selectbox("To Language", ['German', 'Italian'])

    # Display dropdown menu for domain selection (not used in translation)
    domain = st.selectbox("Domain", ['Generic', 'Technology'])

    # Mapping of language names to language codes
    language_codes = {
        'German': 'de',
        'Italian': 'it'
    }

    # File upload
    uploaded_file = st.file_uploader("Upload a Word or PDF file", type=['docx', 'pdf'])

    # Translate file on submit
    if st.button("Translate"):
        if uploaded_file is not None:
            output_file_paths = f"translated_output_{language_codes[to_language]}.txt"
            translated_file_path = translate_file(uploaded_file.name, output_file_paths, language_codes[to_language])
            st.success(f"Translation to {to_language} completed.")
            with open(translated_file_path, "rb") as file:
                file_contents = file.read()
            st.download_button(label="Download Translated File", data=file_contents, file_name=output_file_paths)
        else:
            st.error("Please upload a file first.")

if __name__ == "__main__":
    main()
