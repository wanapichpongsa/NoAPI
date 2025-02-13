import streamlit as st
import ollama
import plotly.express as px
# Document processing
import pdfplumber
import docx
import logging
from performance import monitor_performance, init_performance_monitoring

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
    
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

def log_request(user_messages: list[str], ai_response: str) -> None:
    # Not sure why it implicitly logs HTTP requests...
    logging.info(f"user: {user_messages}")
    logging.info(f"ai: {ai_response}")

# Ideally this should be its own file
def chat():
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
                #print crawl4ai
                
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
                log_request(st.session_state.messages, response["message"]["content"])
                st.session_state.messages.append({"role": "assistant", "content": response["message"]["content"]})
    
@monitor_performance
def main():
    st.title("now.tech")
    from nav import Navigation
    navigation = Navigation()

    if 'registered' not in st.session_state:
        st.session_state.registered = False
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if not st.session_state.registered:
        navigation.nav_to_register()
    elif st.session_state.registered and not st.session_state.logged_in:
        navigation.nav_to_login()
    else:
        navigation.nav_to_main()

    # Sad that routing logic is in the main file. Use page_link when I can.
    from login import login
    from register import register
    if st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'register':
        register()
    elif st.session_state.page == 'main':
        if not st.session_state.get('logged_in', False):
            navigation.nav_to_login()
        else:
            chat()

if __name__ == "__main__":
    observer = init_performance_monitoring()
    try:
        main()
    finally:
        observer.stop()
        observer.join()