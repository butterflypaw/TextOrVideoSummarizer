# Home.py
import streamlit as st

def home():
    st.title("Welcome to Multi-Format Text Summarizer")
    
    if st.session_state.get('logged_in', False):
        st.write(f"Welcome back, {st.session_state['username']}!")
    
    st.write("""
    ## About This Application
    
    This application allows you to:
    - Summarize text from various sources
    - Extract and summarize content from PDF files
    - Summarize YouTube videos (with captions)
    - Generate audiobooks from your summaries
    - Save your summaries for future reference
    - View your summarization history
    
    Get started by logging in or registering a new account.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Text & PDF Support")
        st.write("- Paste any text for summarization")
        st.write("- Upload PDF documents")
        st.write("- Extract text automatically")
    
    with col2:
        st.markdown("### 🎥 YouTube Integration")
        st.write("- Summarize YouTube videos")
        st.write("- Extract video transcripts")
        st.write("- Support for any video with captions")
    
    with col3:
        st.markdown("### 🔊 Audiobook Feature")
        st.write("- Convert summaries to speech")
        st.write("- Download as MP3 files")
        st.write("- Listen on the go")
    
    st.info("The summarizer uses advanced AI models to create concise summaries while maintaining key information.")
    
    # Add example video and PDF information
    with st.expander("ℹ️ How to use YouTube Video Summarization"):
        st.write("""
        1. Copy the YouTube video URL
        2. Paste it in the YouTube section
        3. The app will extract the transcript
        4. Click 'Summarize' to get your summary
        
        Note: The video must have captions/subtitles available.
        """)
    
    with st.expander("ℹ️ How to use PDF Summarization"):
        st.write("""
        1. Upload your PDF file
        2. The app will extract text automatically
        3. Review the extracted text if needed
        4. Click 'Summarize' to get your summary
        
        Note: Works best with text-based PDFs (not scanned images).
        """)
    
    with st.expander("ℹ️ How to use Audiobook Feature"):
        st.write("""
        1. Generate a summary using any method
        2. Check the 'Generate audiobook' option
        3. Listen to the audio or download it
        4. Access audiobooks from your history
        
        Note: The audiobook uses text-to-speech technology.
        """)