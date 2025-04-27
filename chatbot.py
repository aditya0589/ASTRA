import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini (only once)
genai.configure(api_key = st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()

    response = chat.send_message(question, stream=False)

    final_text = response.candidates[0].content.parts[0].text

    return final_text


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
        st.write(response)

        st.session_state['chat_history'].append(("Bot", response))
