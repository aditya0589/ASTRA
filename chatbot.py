import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini with your API key (set this in your environment variables)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model and start a chat session
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# Function to get response
def get_gemini_response(question):
    lowered = question.strip().lower()

    # Custom hardcoded responses
    if lowered in ["who created you", "who made you", "who is your creator", "who developed you"]:
        return "I was developed by Aditya."

    # Gemini streamed response
    return chat.send_message(question, stream=True)

# Streamlit app
def show_chatbot():
    st.title("ASTRA - Your AI Chatbot")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = []

    # Show chat history in sidebar
    st.sidebar.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        with st.sidebar.expander(f"{role}", expanded=False):
            st.write(text)

    # Input from user
    input_text = st.text_input("Ask me anything...", key='input')
    submit = st.button("Ask")

    if submit and input_text:
        response = get_gemini_response(input_text)

        # Add user input to chat history
        st.session_state['chat_history'].append(("You", input_text))

        st.subheader("The Response:")
        complete_response = ""

        # Handle custom vs Gemini streamed response
        if isinstance(response, str):
            st.write(response)
            complete_response = response
        else:
            for chunk in response:
                st.write(chunk.text)
                complete_response += chunk.text

        # Add bot response to chat history
        st.session_state['chat_history'].append(("Bot", complete_response))

# Run the chatbot app
if __name__ == "__main__":
    show_chatbot()
