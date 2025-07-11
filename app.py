import streamlit as st
from PIL import Image
import re

# Placeholder imports for OCRFlux
# from ocrflux.ocr_engines import TesseractEngine
# from ocrflux.pipeline import OCRPipeline
# from ocrflux.parsers import LineParser

# Set page config
st.set_page_config(page_title="Menu Digitizer", layout="centered")

# Title and instructions
st.title("📸 Menu Card Digitizer")
st.write("Upload an image of a menu card, and we'll extract the items and prices.")

# Upload image
uploaded_file = st.file_uploader("Choose a menu image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Menu", use_container_width=True)

    # OCR Processing placeholder
    with st.spinner("🔍 Reading text with OCR (using Tesseract)..."):
        # Use pytesseract here as placeholder for OCRFlux integration later
        import pytesseract
        ocr_text = pytesseract.image_to_string(image, lang="dan+eng")

    # Split OCR output into lines for regex processing
    lines = ocr_text.splitlines()

    # Extract item–price pairs using regex
    menu_items = []
    pattern = re.compile(r"(.+?)\s+(\d+[.,]?\d*\s*(kr|dkk|DKK)?)", flags=re.IGNORECASE)
    for line in lines:
        text = line.strip()
        match = pattern.match(text)
        if match:
            item = match.group(1).strip()
            price = match.group(2).strip()
            menu_items.append({"Item": item, "Price": price})

    # Display results
    if menu_items:
        st.success("✅ Items and prices extracted successfully!")
        st.dataframe(menu_items, use_container_width=True)
    else:
        st.warning("🤔 Could not detect any item–price pairs. Try a clearer image or a different format.")
else:
    st.info("Please upload a menu image to get started.")
