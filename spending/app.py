import streamlit as st
import pandas as pd
import ollama
import plotly.express as px
# Document processing
import pdfplumber
import docx
import sqlite3
import logging
import json
    
def read_file(uploaded_file):
    # Warning: Not typesafe
    if uploaded_file.type == "application/pdf":
         with pdfplumber.open(uploaded_file) as pdf:
            return " ".join(page.extract_text() for page in pdf.pages)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return " ".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        return uploaded_file.getvalue().decode()

def main():
    st.title("now.tech")
    # Add custom CSS to resize file uploader
    st.markdown("""
        <style>
        .stFileUploader div[data-testid="stFileUploadDropzone"] {
            min-height: 100px;
            max-height: 100px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    **NOTICE:** It is recommended to name your file in the format of 'Month(3-4 characters) Year(4 digits).pdf' e.g., 'Jan 2025.pdf'
    """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # File uploader and chat input in columns
    col1, col2 = st.columns([3, 1])
    # Chat input
    model = 'deepseek-r1:8b'
    document_text = None
    with col2:
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "docx", "pdf"])
        if uploaded_file:
            document_text = read_file(uploaded_file)

    with col1:
        if prompt := st.chat_input("What ELT process would you like for me to perform?"):
            if not document_text:
                st.session_state.messages.append({"role": "user", "content": prompt})
            else:
                st.session_state.messages.append({"role": "user", "content": prompt + "\n" + document_text})

            with st.chat_message("user"):
                if not document_text:
                    st.markdown(prompt)
                else:
                    st.markdown(prompt + "\n" + document_text)
                

            with st.chat_message("assistant"):
                llm = ollama.Client()
                response = llm.chat(model=model, messages=st.session_state.messages)
                st.markdown(response["message"]["content"])

            st.session_state.messages.append({"role": "assistant", "content": response["message"]["content"]})

if __name__ == "__main__":
    main()