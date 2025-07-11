import streamlit as st
from PIL import Image
import re

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

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

    # OCR Processing with Doctr
    with st.spinner("🔍 Reading text with OCR (Doctr)..."):
        doc = DocumentFile.from_images(image)
        model = ocr_predictor(pretrained=True)
        result = model(doc)
        text_lines = result.pages[0].extract_words()

    # Extract item–price pairs using regex
    menu_items = []
    for word in text_lines:
        line = word["value"].strip()
        match = re.match(r"(.+?)\s+(\d+[.,]?\d*\s*(kr|dkk|DKK)?)", line, flags=re.IGNORECASE)
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
