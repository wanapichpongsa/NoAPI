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

def run_agent(prompt: str = None, attachment: str = None) -> None:
    from agent import ConversationalAgent
    agent = ConversationalAgent()
    while True:
      if not prompt:
        user_input = input("You: ")
        if user_input == "exit":
          return
        elif user_input == "new agent":
          last_context = agent.get_latest_response()
          run_agent(None, last_context) # RECURSION
        agent.conversation(user_input, attachment) # no recursion since need same agent instance
      else:
        agent.conversation(prompt, attachment)
        run_agent(None, None) # RECURSION
    
def main():
  try:
    start_time = time.time()

    data_dir = "../database/documents/bank_statements"
    first_file = os.listdir(data_dir)[0]
    pages = get_pdf_pages(data_dir + "/" + first_file)
    first_prompt = "Output the first and last line of the invoice table in this bank statement document and explain why you chose them:"
    run_agent(first_prompt, pages[0])
  finally:
    end_time = time.time()
    logging.info(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
  main()