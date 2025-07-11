import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import re

# Page config
st.set_page_config(page_title="Menu Digitizer", layout="centered")

st.title("📸 Menu Card Digitizer")
st.write("Upload an image of a menu card, and we'll extract the items and prices.")

uploaded_file = st.file_uploader("Choose a menu image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Menu", use_container_width=True)

    with st.spinner("🔍 Reading text with OCR..."):
        reader = easyocr.Reader(['da', 'en'], gpu=False)
        results = reader.readtext(np.array(image), detail=0)

    # Extract item–price pairs using regex
    menu_items = []
    for text in results:
        clean_text = text.strip()
        match = re.match(r"(.+?)\s+(\d+[.,]?\d*\s*(kr|dkk|DKK)?)", clean_text, flags=re.IGNORECASE)
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
