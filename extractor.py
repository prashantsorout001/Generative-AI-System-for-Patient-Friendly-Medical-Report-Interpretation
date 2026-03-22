import streamlit as st
from PIL import Image
import pytesseract
import json
from transformers import pipeline
# from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_model()

st.set_page_config(page_title="Invoice Information Extractor", layout="wide")
st.title("📑 Invoice Information Extractor")

# Load HuggingFace model
# generator = pipeline("text-generation", model="google/flan-t5-base")


# OCR FUNCTION
def extract_text_from_file(uploaded_file):
    try:
        image = Image.open(uploaded_file)

        # Convert image to grayscale
        gray_image = image.convert("L")

        text = pytesseract.image_to_string(gray_image)

        return text

    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None


# AI PROCESSING FUNCTION
def process_with_ai(text):

    prompt = f"""
Extract invoice information and convert to JSON.

Fields:
invoice_number
invoice_date
vendor_name
total_amount

Invoice Text:
{text}
"""

    result = generator(prompt, max_length=256)

    return result[0]["generated_text"]


uploaded_file = st.file_uploader("Upload Invoice Image", type=["png", "jpg", "jpeg"])


if uploaded_file:

    st.image(uploaded_file, caption="Uploaded Invoice", use_column_width=True)

    if st.button("Extract Information"):

        with st.spinner("Extracting text from image..."):

            extracted_text = extract_text_from_file(uploaded_file)

        if extracted_text:

            st.subheader("🔎 Extracted Text")
            st.text(extracted_text)

            st.subheader("🤖 Processing with HuggingFace AI...")

            ai_output = process_with_ai(extracted_text)

            st.subheader("📋 AI Output")
            st.text(ai_output)

            try:
                json_data = json.loads(ai_output)

                st.subheader("📊 Extracted JSON")
                st.json(json_data)

                st.download_button(
                    label="Download JSON",
                    data=json.dumps(json_data, indent=4),
                    file_name="invoice_data.json",
                    mime="application/json"
                )

            except:
                st.warning("AI output JSON format me nahi tha.")