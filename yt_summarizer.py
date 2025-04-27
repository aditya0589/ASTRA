# yt_summarizer.py

import streamlit as st  # Added for Streamlit UI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the Gemini model
prompt = """
You are a YouTube video summarizer. You will be taking the transcript text 
and summarizing the entire video and providing the entire summary in points 
within 200 to 250 words. The transcript text will be provided here:
"""

# Getting the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        if "watch?v=" in youtube_video_url:
            video_id = youtube_video_url.split("=")[1]
        elif "youtu.be/" in youtube_video_url:
            video_id = youtube_video_url.split("/")[-1]
        else:
            raise ValueError("Invalid YouTube URL format.")

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript

    except Exception as e:
        raise e

# Getting the summary based on the prompt
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt + transcript_text])
    return response.candidates[0].content.parts[0].text

# Streamlit page function to connect with your app
def show_youtube_summarizer():
    """
    Streamlit UI to summarize YouTube videos.
    """
    st.header("YouTube Video Summarizer")

    youtube_url = st.text_input("Enter the YouTube video URL:")

    if youtube_url:
        try:
            with st.spinner('Fetching transcript...'):
                transcript = extract_transcript_details(youtube_url)
                st.success("Transcript fetched successfully!")

            with st.spinner('Summarizing...'):
                summary = generate_gemini_content(transcript, prompt)
                st.subheader("Summary:")
                st.write(summary)

                st.download_button(
                    label="Download Summary as Text",
                    data=summary,
                    file_name="youtube_summary.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error: {e}")
