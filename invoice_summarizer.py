import streamlit as st

def show_invoice_summarizer():
    st.title("Multi-language Invoice Summarizer")
    uploaded_invoice = st.file_uploader("Upload your invoice (PDF)", type=["pdf"])
    language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Hindi"])
    if uploaded_invoice and st.button("Summarize Invoice"):
        st.success(f"Summarizing invoice in {language} (Summarization logic to be added.)")

