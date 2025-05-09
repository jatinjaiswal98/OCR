import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import io
import os
import base64
from datetime import datetime

st.set_page_config(page_title="Vendor Onboarding", layout="wide")

st.title("📋 Vendor Onboarding Portal")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []

st.subheader("Vendor Information")

vendor_name = st.text_input("Vendor Name")
email = st.text_input("Email")
category = st.selectbox("Category", ["Goods", "Services", "Consulting", "Others"])

st.subheader("Upload Required Documents")
trade_license = st.file_uploader("Upload Trade License (PDF/Image)", type=["png", "jpg", "jpeg", "pdf"])
bank_proof = st.file_uploader("Upload Cancelled Cheque / Bank Proof", type=["png", "jpg", "jpeg", "pdf"])
gst_cert = st.file_uploader("Upload GST Certificate", type=["png", "jpg", "jpeg", "pdf"])


def extract_text(file):
    try:
        if file.type.startswith("image"):
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            return text
        else:
            return "[PDF parsing not implemented in demo]"
    except Exception as e:
        return f"Error: {e}"


def score_documents(*docs):
    score = 0
    total = len(docs)
    for doc in docs:
        if doc:
            score += 1
    return int((score / total) * 100)


if st.button("Submit Vendor Info"):
    if vendor_name and email:
        trade_text = extract_text(trade_license) if trade_license else "Not uploaded"
        bank_text = extract_text(bank_proof) if bank_proof else "Not uploaded"
        gst_text = extract_text(gst_cert) if gst_cert else "Not uploaded"

        score = score_documents(trade_license, bank_proof, gst_cert)

        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vendor Name": vendor_name,
            "Email": email,
            "Category": category,
            "Score": f"{score}%",
            "Trade License Extract": trade_text[:100],
            "Bank Proof Extract": bank_text[:100],
            "GST Extract": gst_text[:100]
        }

        st.session_state.data.append(record)
        st.success(f"Vendor data submitted successfully with score: {score}%")
    else:
        st.error("Please fill in all required fields.")


st.subheader("Submitted Vendors")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="vendor_submissions.csv">📥 Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.info("No vendor submissions yet.")
