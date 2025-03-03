import pdfplumber
import os
import json
from sentence_transformers import SentenceTransformer
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pdf_pages(path: str) -> list:
  pages = []
  with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
      pages.append(page.extract_text())
  return pages

def create_embeddings(pages: list) -> list:
  model = SentenceTransformer('all-MiniLM-L6-v2')
  logging.info("Creating embeddings...")
  embeddings = model.encode(pages)
  return embeddings

# TODO: GET MOST LIKELY PAGE -> LINES

def ollama_extract_table(page: str) -> json:
    logging.info("Fetching Ollama response...")
    client = ollama.Client()
    response = client.chat(
        model="llama3.2:latest",
        messages=[{
            "role": "user",
            "content": f"Extract the invoice tables from this text as JSON. Focus on numerical data and columnar patterns:\n{page}"
        }],
        format="json"
    )
    message = response.message.content
    return json.dumps(json.loads(message, strict=False), indent=4)


def main():
  try:
    start_time = time.time()

    data_dir = "../data/"
    first_file = os.listdir(data_dir)[0]
    pages = get_pdf_pages(data_dir + first_file)

    from agent import ConversationalAgent
    agent = ConversationalAgent()
    agent.conversation(pages[0])
    while True:
      agent.conversation()
  finally:
    end_time = time.time()
    logging.info(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
  main()