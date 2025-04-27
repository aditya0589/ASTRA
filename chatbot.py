import streamlit as st
import google.generativeai as genai

# Configure Gemini (only once)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """Send a message to Gemini and get a response."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()

    response = chat.send_message(
        question,    # just the text
        stream=False # no streaming, simple output
    )

    return response.text  # directly get the text

def show_chatbot():
    """Display the chatbot interface in Streamlit."""
    st.title("ASTRA - Your AI Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = []

    # Show chat history in sidebar
    st.sidebar.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        with st.sidebar.expander(f"{role}", expanded=False):
            st.write(text)

    # Input from user
    input_text = st.text_input("Ask me anything...", key='input')

    # Submit button
    submit = st.button("Ask")

    if submit and input_text:
        # Get response
        response = get_gemini_response(input_text)

        # Save user message
        st.session_state['chat_history'].append(("You", input_text))

        # Display bot response
        st.subheader("The Response:")
        st.write(response)

        # Save bot message
        st.session_state['chat_history'].append(("Bot", response))
