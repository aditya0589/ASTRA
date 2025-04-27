import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini (only once)
genai.configure(api_key = st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(
    [
        {
            "role": "user",
            "parts": [{"text": question}]
        }
    ],
    stream=True
)

    return response

def show_chatbot():
    st.title("ASTRA - Your AI Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = []

    st.sidebar.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        with st.sidebar.expander(f"{role}", expanded=False):
            st.write(text)

    input_text = st.text_input("Ask me anything...", key='input')

    submit = st.button("Ask")

    if submit and input_text:
        response = get_gemini_response(input_text)

        st.session_state['chat_history'].append(("You", input_text))

        st.subheader("The Response:")
        complete_response = ""
        for chunk in response:
            st.write(chunk.text)
            complete_response += chunk.text

        st.session_state['chat_history'].append(("Bot", complete_response))
