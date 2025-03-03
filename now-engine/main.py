import pdfplumber
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pdf_pages(path: str) -> list:
  pages = []
  with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
      pages.append(page.extract_text())
  return pages

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