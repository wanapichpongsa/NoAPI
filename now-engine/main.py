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
    first_prompt = "Output the first and last line of the invoice table in this bank statement document and explain why you chose them:"
    agent.conversation(first_prompt, pages[0])
    while True:
      user_input = input("You: ")
      if user_input == "exit":
        break
      agent.conversation(user_input)
      if user_input == "new agent":
        last_context = agent.get_latest_response()
        agent = ConversationalAgent()  # Replace the old agent
        user_input = input("You: ")
        if user_input == "exit":
          break
        agent.conversation(user_input, last_context)

  finally:
    end_time = time.time()
    logging.info(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
  main()