import streamlit as st
import pandas as pd
import ollama
import plotly.express as px
# Document processing
import pdfplumber
import docx
import sqlite3
import logging
llm = ollama.Client()
def process_with_llm(text):
    system_prompt = """You are a financial data analyst. Your tasks:
    1. Extract transaction data from bank statement documents (e.g., txt, pdf, csv, xml, word) common columns are: date, details, outflow, inflow, balance.
    2. Categorize transactions into hierarchical groups:
        - essentials: {groceries, utilities, rent}
        - transport: {fuel, public_transport, car_maintenance}
        - leisure: {dining, entertainment, shopping}
    3. Very concisely explain your categorization logic
    4. Return data in JSON format:
        {
            "transactions": [...],
            "categories": {...},
            "reasoning": "..."
        }
    """
    
    try:
        # system is overall behaviour, user is specific messages.
        # see existing models: https://ollama.com/library/deepseek-r1
        response = llm.chat(model="deepseek-r1:8b", messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Process this bank statement:\n{text}"}
        ])
        return response["message"]["content"]
    except Exception as e:
        raise e
    
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
    uploaded_file = st.file_uploader("Upload document (txt, csv, docx, pdf)", 
                                   type=["txt", "csv", "docx", "pdf"],
                                   accept_multiple_files=False)
    if uploaded_file:
        text = read_file(uploaded_file)
        # get filename to determine table name
        filename = uploaded_file.name
        filename = filename.split('.')[0]
        tablename = None
        import re
        month_year_pattern = re.compile(r'[a-zA-Z]{3,4} \d{2,4}')
        find_pattern = month_year_pattern.search(filename)
        if find_pattern:
            tablename = "_".join(find_pattern.group(0).split(" "))
        else:
            tablename = "_".join(filename.split(" "))
            

        with st.spinner("Processing..."):
            analysis = process_with_llm(text)
            st.write('### LLM Analysis')
            st.write(analysis)

        # save to local database
        model = 'deepseek-coder:1.3b'
        conn = sqlite3.connect('processed_data.db')
        df = pd.DataFrame({
            'original_text': [text],
            f'{model}_output': [analysis],
            'filename': [uploaded_file.name]
        })
        df.to_sql(tablename, conn, if_exists='append', index=False)
        st.success("Data saved to database")

        # display data
        st.write("### Processed Data")
        st.dataframe(pd.read_sql_query(f"SELECT * FROM {tablename}", conn)) # quote table name if you want spaces.

        # Export to excel (hope API downloads, and configures to 2 sheets)
        df.to_excel(f"{tablename}.xlsx", index=False)

        # Visualise data
        # fig_inflow = px.pie(df, values='inflow', names='category', title='Spending by Category')
        # fig_outflow = px.pie(df, values='outflow', names='category', title='Spending by Category')
        # st.plotly_chart(fig_inflow)
        # st.plotly_chart(fig_outflow)

        # Append additional data
        st.write("### Append additional data")
        additional_data = st.file_uploader("Upload additional data", type=["csv", "xlsx", "txt", "docx", "pdf"])
        if additional_data:
            logging.warning('We\'re not ready to append data yet')

if __name__ == "__main__":
    main()