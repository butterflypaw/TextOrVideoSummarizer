import streamlit as st
import load
from langchain_community.document_loaders import YoutubeLoader
url=st.text_input("Enter the url",placeholder="URL....")
if url:
    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info=False
    )
    transcript=loader.load()
    response=load.output(str(transcript))
    for chunk in response:
        st.write(chunk.text)