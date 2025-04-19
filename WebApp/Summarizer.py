# Summarizer.py
import streamlit as st
import requests
from Database import save_summary
import PyPDF2
import io
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse
import re
from gtts import gTTS
import base64

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\n?]*)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    """Get transcript from YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([entry['text'] for entry in transcript_list])
        return transcript
    except Exception as e:
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + " "
        return text
    except Exception as e:
        return None

def text_to_speech(text):
    """Convert text to speech and return audio data."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        return None

def summarizer():
    st.title("Summarizer")
    
    if not st.session_state.get('logged_in', False):
        st.warning("Please login to use the summarizer")
        return
    
    # Tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Text", "PDF", "YouTube Video"])
    
    with tab1:
        st.subheader("Text Summarization")
        text_input = st.text_area("Enter text to summarize:", height=300)
    
    with tab2:
        st.subheader("PDF Summarization")
        pdf_file = st.file_uploader("Upload a PDF file", type=['pdf'])
        if pdf_file:
            text_input = extract_text_from_pdf(pdf_file)
            if text_input:
                st.success("PDF text extracted successfully!")
                with st.expander("View extracted text"):
                    st.write(text_input[:1000] + "..." if len(text_input) > 1000 else text_input)
            else:
                st.error("Could not extract text from PDF")
    
    with tab3:
        st.subheader("YouTube Video Summarization")
        youtube_url = st.text_input("Enter YouTube video URL:")
        if youtube_url:
            video_id = extract_video_id(youtube_url)
            if video_id:
                transcript = get_transcript(video_id)
                if transcript:
                    text_input = transcript
                    st.success("Video transcript extracted successfully!")
                    with st.expander("View transcript"):
                        st.write(transcript[:1000] + "..." if len(transcript) > 1000 else transcript)
                else:
                    st.error("Could not extract transcript. Make sure the video has captions enabled.")
            else:
                st.error("Invalid YouTube URL")
    
    # Summarizer settings
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox("Summary Length:", ["Short", "Medium", "Long"])
    with col2:
        summarization_method = st.selectbox("Summarization Method:", ["Extractive", "Abstractive"])
    
    # Add checkbox for audiobook generation
    create_audiobook = st.checkbox("Generate audiobook of summary", value=False)
    
    if st.button("Summarize"):
        if text_input:
            with st.spinner("Generating summary..."):
                try:
                    # Call the Flask API running in Docker at localhost:5000
                    response = requests.post(
                        "http://localhost:5000/summarize",
                        json={
                            "text": text_input,
                            "length": summary_length.lower(),
                            "method": summarization_method.lower()
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        summary = response.json().get('summary', '')
                        st.success("Summary generated successfully!")
                        st.markdown("### Summary")
                        st.write(summary)
                        
                        # Save to history
                        save_summary(st.session_state['user_id'], text_input, summary)
                        
                        # Download button for summary
                        st.download_button(
                            label="Download Summary",
                            data=summary,
                            file_name="summary.txt",
                            mime="text/plain"
                        )
                        
                        # Generate audiobook if requested
                        if create_audiobook:
                            with st.spinner("Generating audiobook..."):
                                audio_buffer = text_to_speech(summary)
                                if audio_buffer:
                                    st.markdown("### Audiobook")
                                    st.audio(audio_buffer, format='audio/mp3')
                                    
                                    # Convert audio to base64 for download
                                    audio_base64 = base64.b64encode(audio_buffer.read()).decode()
                                    audio_buffer.seek(0)
                                    href = f'<a href="data:audio/mp3;base64,{audio_base64}" download="summary_audiobook.mp3">Download Audiobook</a>'
                                    st.markdown(href, unsafe_allow_html=True)
                                else:
                                    st.error("Could not generate audiobook")
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the summarization service. Please make sure the Docker container is running.")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The text might be too long.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please provide content to summarize")