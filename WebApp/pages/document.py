import streamlit as st
import document_data
import load
data=document_data.document_extract()
if data:
    response=(load.output(data))
    for chunk in response:
        st.write(chunk.text)