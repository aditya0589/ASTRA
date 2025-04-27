from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# Import service modules
import chatbot
import pdf_summarizer
import yt_summarizer
import invoice_summarizer
import nutrition_assistant
import picture_summarizer  # NEW IMPORT

# Initialize app
st.set_page_config(page_title="ASTRA - AI Multi-Tool", layout="wide")

st.sidebar.title("ASTRA - Navigation")

# Initialize session states
if "page" not in st.session_state:
    st.session_state.page = "Chatbot"

if "history" not in st.session_state:
    st.session_state.history = []  # <-- Initialize history tracker

# Function to log page visits
def log_page_visit(page_name):
    st.session_state.history.append(page_name)

# Navigation Buttons
if st.sidebar.button("Chatbot"):
    st.session_state.page = "Chatbot"
    log_page_visit("Chatbot")

if st.sidebar.button("PDF Summarizer"):
    st.session_state.page = "PDF Summarizer"
    log_page_visit("PDF Summarizer")

if st.sidebar.button("YouTube Summarizer"):
    st.session_state.page = "YouTube Summarizer"
    log_page_visit("YouTube Summarizer")

# if st.sidebar.button("Invoice Summarizer"):
#     st.session_state.page = "Invoice Summarizer"
#     log_page_visit("Invoice Summarizer")

# if st.sidebar.button("Nutrition Assistant"):
#     st.session_state.page = "Nutrition Assistant"
#     log_page_visit("Nutrition Assistant")

if st.sidebar.button("Picture Summarizer"):
    st.session_state.page = "Picture Summarizer"
    log_page_visit("Picture Summarizer")

# Render selected page
if st.session_state.page == "Chatbot":
    chatbot.show_chatbot()

elif st.session_state.page == "PDF Summarizer":
    pdf_summarizer.show_pdf_summarizer()

elif st.session_state.page == "YouTube Summarizer":
    yt_summarizer.show_youtube_summarizer()

# elif st.session_state.page == "Invoice Summarizer":
#     invoice_summarizer.show_invoice_summarizer()

# elif st.session_state.page == "Nutrition Assistant":
#     nutrition_assistant.show_nutrition_assistant()

elif st.session_state.page == "Picture Summarizer":
    picture_summarizer.show_picture_summarizer()

# History Section
with st.expander("View Your Activity History"):
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history, 1):
            st.write(f"{i}. {entry}")
    else:
        st.write("No activity yet!")
