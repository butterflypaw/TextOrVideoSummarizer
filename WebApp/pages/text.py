import load
import streamlit as st
text=st.text_input("Enter the text you want to summarize..")
if text:
    response=(load.output(text))
    for chunk in response:
        st.write(chunk.text)