import streamlit as st
from PyPDF2 import PdfReader
import docx2txt
def document_extract():
    uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True)
    content = """"""
    if uploaded_file is not None:
        for x in uploaded_file:
            if(x.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
                content += docx2txt.process(x)
            elif(x.type=="application/pdf"):
                pdf_reader = PdfReader(x)
                for page_num in range(len(pdf_reader.pages)):
                    content += pdf_reader.pages[page_num].extract_text()
            elif(x.type=="text/plain"):
                content = st.read(x)
            else:
                st.error("Please provide files of type **.docx**,**.pdf**,**.txt**")
    return content
