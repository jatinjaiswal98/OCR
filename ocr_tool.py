import streamlit as st

st.set_page_config(page_title="Free OCR Tool", layout="centered")
st.title("🧾 Free OCR Tool")

try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np

    uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.info("Image uploaded. Processing...")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

        st.success("✅ Text extraction complete!")
        st.subheader("📝 Extracted Text:")
        st.text_area("", text, height=300)
    else:
        st.warning("👈 Please upload an image file to begin.")

except Exception as e:
    st.error(f"🚨 App failed to load properly. Error: {e}")
