import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Utility Functions ---

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the given question as detailed as possible from the provided context. Make sure to provide all the details.
    If the answer is not available in the context, just say "Answer is not available in the context."
    Do not make up information.

    Context:
    {context}

    Question: 
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type='stuff', prompt=prompt)
    return chain

def answer_user_question(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

# --- Main function to show in app ---

def show_pdf_summarizer():
    st.header("Chat with your PDFs")

    st.write(
        "Upload PDF files in the sidebar, then ask any questions related to them!"
    )

    user_question = st.text_input("Ask a question related to your uploaded PDFs:")

    if user_question:
        try:
            with st.spinner('Searching for answer...'):
                reply = answer_user_question(user_question)
                st.subheader("Reply:")
                st.write(reply)
        except Exception as e:
            st.error("Please upload and process PDF(s) first before asking questions.")

    with st.sidebar:
        st.subheader("Upload and Process PDFs")
        pdf_docs = st.file_uploader("Upload PDF files", accept_multiple_files=True)

        if st.button("⚡ Submit and Process PDFs"):
            if pdf_docs:
                with st.spinner("⏳ Processing your PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("✅ PDFs processed successfully! You can now ask questions.")
            else:
                st.warning("Please upload at least one PDF file first.")

