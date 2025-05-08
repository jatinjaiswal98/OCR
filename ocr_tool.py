import streamlit as st
from datetime import datetime
from PIL import Image
import easyocr
import pdf2image
import tempfile
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize OCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Set up Google Sheets API
def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds/credentials.json", scope)
    client = gspread.authorize(creds)
    return client

def append_to_gsheet(sheet_id, file_name, text):
    client = get_gsheet_client()
    sheet = client.open_by_key(sheet_id).sheet1
    now = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([file_name, text, now])

# OCR function for image
def extract_text_from_image(image):
    result = reader.readtext(image, detail=0)
    return "\n".join(result)

# OCR function for PDF
def extract_text_from_pdf(uploaded_pdf):
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_bytes(uploaded_pdf.read(), dpi=300, output_folder=path)
        text = ""
        for img in images:
            result = reader.readtext(img, detail=0)
            text += "\n".join(result) + "\n"
    return text

# Streamlit UI
st.title("📄 OCR to Google Sheets Tool")

sheet_id = st.text_input("Enter your Google Sheet ID", "")

uploaded_file = st.file_uploader("Upload an image or PDF file", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file and sheet_id:
    file_name = uploaded_file.name
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        text = extract_text_from_image(image)

    st.text_area("Extracted Text", text, height=300)

    if st.button("Send to Google Sheet"):
        try:
            append_to_gsheet(sheet_id, file_name, text)
            st.success("✅ Data sent to Google Sheet!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
