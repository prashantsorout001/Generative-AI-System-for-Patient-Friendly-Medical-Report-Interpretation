import streamlit as st
st.set_page_config(page_title="Medical Report OCR to Table", layout="centered")

from paddleocr import PaddleOCR
from PIL import Image
import requests
import numpy as np

# -----------------------------
# GitHub Token
# -----------------------------

github_token = st.secrets["github_token"]

# -----------------------------
# Load PaddleOCR
# -----------------------------

ocr = PaddleOCR(use_angle_cls=True, lang='en')

# -----------------------------
# OCR Function
# -----------------------------

def extract_text(image):

    result = ocr.ocr(np.array(image))

    text_lines = []

    for line in result:
        for word in line:
            text_lines.append(word[1][0])

    extracted_text = "\n".join(text_lines)

    return extracted_text


# -----------------------------
# GitHub Model Table Generator
# -----------------------------

def format_text_to_table(extracted_text):

    url = "https://models.github.ai/inference/chat/completions"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a medical lab report parser.

The following text is extracted from a blood test report using OCR.
OCR text may contain spelling mistakes.

Your job:

1. Identify blood test parameters (RBC, WBC, HGB, HCT, MCV, MCH, MCHC, RDW etc.)
2. Extract the test value.
3. Extract the reference range.
4. Ignore unrelated text like "Slide Review", "Signature".

Return ONLY a clean markdown table.

Columns:

Test | Value | Reference Range

OCR TEXT:
{extracted_text}
"""

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:

        result = response.json()

        return result["choices"][0]["message"]["content"]

    else:

        st.error(response.text)

        return None


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("Medical Report OCR → Table Generator")

st.write("Upload a medical report image to extract text and convert it into a structured table.")

uploaded_file = st.file_uploader(
    "Upload image", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image")

    # OCR
    with st.spinner("Extracting text using PaddleOCR..."):

        extracted_text = extract_text(image)

    st.subheader("Extracted Text")

    st.text_area("OCR Output", extracted_text, height=250)

    # Table generation
    with st.spinner("Generating Table using AI..."):

        table = format_text_to_table(extracted_text)

    if table:

        st.subheader("Generated Table")

        st.markdown(table)