import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini once
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from Gemini model
def get_gemini_response(input_text, image):
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

def show_picture_summarizer():
    st.title("Picture Summarizer - ASTRA")
    st.write("Upload an image and optionally give a prompt to get a smart summary!")

    input_text = st.text_input("Enter an optional prompt (e.g., 'Summarize this image')", key="image_input")

    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpeg', 'jpg'])

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)

    submit = st.button("Summarize Image")

    if submit:
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner('Generating summary...'):
                response = get_gemini_response(input_text, image)
                st.subheader("Summary:")
                st.write(response)

