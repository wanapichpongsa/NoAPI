"""
For UV
add $HOME/.local/bin 
source $HOME/.local/bin/env (sh, bash, zsh)
"""

import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from typing import List, Dict, Optional
import pdfplumber
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# There are 3 line transactions (see Apple one)
# Problem: Refunds (e.g., LI has type 'VIS')

# Insert your folder paths
folders: str = []

def extract_transactions(text: str) -> List[str]:
    lines = text.split('\n')
    transactions = []
    current_transaction: Dict[str, str | float] = {
              'date': None, # retrieve the first instance
              'payment_type': '',
              'details': '',
              'paid_out': None,
              'paid_in': None,
              'balance': None
            }

    date_pattern = re.compile(r'(\d{2} [a-zA-Z]{3} \d{2})')
    current_date = None
    # previous pattern: \d+\.\d{2}
    """
      Regex explanation:
        1. (?<!\d%) - negative lookbehind: don't match if preceded by digit and %
        2. \b - word boundary
        3. \d+\.\d{2} - the float number pattern
        4. \b - word boundary
        5. (?!%) - negative lookahead: don't match if followed by %
    """
    float_pattern = re.compile(r'(?<!\d%)\b\d+\.\d{2}\b(?!%)')  # Match floats not followed by % and not preceded by digit%

    for line in lines:
        logging.info(line)
        # skip header line and empty lines
        line = line.replace(',', '') # so , not in numbers.

        if 'Date Payment type and details' in line or line.strip() == '':
              continue
        # Check if line starts with a date
        date_match = date_pattern.match(line)
        amounts = float_pattern.findall(line)

        if date_match:
            # Extract rest of the line after date
            current_date = date_match.group(1)
            rest_of_line = line[date_match.end()+1:].strip()
            
            # restarts everytime there is a new date.
            current_transaction: Dict[str, str | float] = {
              'date': current_date, # retrieve the first instance
              'payment_type': '',
              'details': '',
              'paid_out': None,
              'paid_in': None,
              'balance': None
            }
            parts = rest_of_line.split(' ')
            if parts:
                current_transaction['payment_type'] = parts[0]
                current_transaction['details'] = ' '.join(parts[1:])
                # transaction amounts do not ever exist in the same line as date.

            # specially handle balance brought forward and balance carried forward
            # just take the repeated code
            if 'BALANCE BROUGHT FORWARD' in rest_of_line:
                current_transaction['payment_type'] = 'BALANCE BROUGHT FORWARD'
                amounts = float_pattern.findall(rest_of_line)
                if amounts:
                    current_transaction['balance'] = float(amounts[0])
                else: raise ValueError(f"No balance found in {line}")
                continue
            elif 'BALANCE CARRIED FORWARD' in rest_of_line:
                current_transaction['payment_type'] = 'BALANCE CARRIED FORWARD'
                amounts = float_pattern.findall(rest_of_line)
                if amounts:
                    current_transaction['balance'] = float(amounts[0])
                else: raise ValueError(f"No balance found in {line}")
                continue
            
        elif not date_match and current_date:
            parts = line.split(' ')
            if amounts: # this logic isn't valid because even if new date, same line won't have amounts 
                if current_transaction['details']: # there are details before amount
                    # regex vectors don't have a start() method
                    try:
                        parts.index(amounts[0])
                    except ValueError as e:
                        raise ValueError(f"No details found in {line}, amount = {amounts}") from e
                    current_transaction['details'] = ' '.join(parts[:parts.index(amounts[0])])
                
                # This is conditions for transaction amounts. Make sure to make values that didn't appear in line None
                if current_transaction['payment_type'] == 'CR': # CR is only instance of paid in
                    if len(amounts) == 2:
                        current_transaction['paid_out'] = None
                        current_transaction['paid_in'] = float(amounts[0])
                        current_transaction['balance'] = float(amounts[-1])
                    elif len(amounts) == 1:
                        current_transaction['paid_out'] = None
                        current_transaction['balance'] = None
                        current_transaction['paid_in'] = float(amounts[0])
                else:
                    if len(amounts) == 2:
                        current_transaction['paid_in'] = None
                        current_transaction['paid_out'] = float(amounts[0])
                        current_transaction['balance'] = float(amounts[-1])
                    elif len(amounts) == 1:
                        current_transaction['paid_in'] = None
                        current_transaction['balance'] = None
                        current_transaction['paid_in'] = float(amounts[0])
                # specially handle balance brought forward and balance carried forward
                # just take the repeated code
                if 'BALANCE BROUGHT FORWARD' in rest_of_line:
                    current_transaction['payment_type'] = 'BALANCE BROUGHT FORWARD'
                    amounts = float_pattern.findall(rest_of_line)
                    if amounts:
                        current_transaction['balance'] = float(amounts[0])
                    else: raise ValueError(f"No balance found in {line}")
                    continue
                elif 'BALANCE CARRIED FORWARD' in rest_of_line:
                    current_transaction['payment_type'] = 'BALANCE CARRIED FORWARD'
                    amounts = float_pattern.findall(rest_of_line)
                    if amounts:
                        current_transaction['balance'] = float(amounts[0])
                    else: raise ValueError(f"No balance found in {line}")
                    continue
                transactions.append(current_transaction)
            elif parts[0] == ')))':
                current_transaction['payment_type'] = parts[0]
                current_transaction['details'] = ' '.join(parts[1:])
            else:
                current_transaction['details'] += ' ' + line

    return transactions

def init_file_paths(folders: List[str]) -> Dict[str, List[str]]:
  file_paths: Dict[str, List[str]] = {}
  for folder in folders:
      folder_paths = []
      for file in os.listdir(folder):
          if file.endswith('.pdf'):
              folder_paths.append(os.path.join(folder, file))
      year = folder.split('/')[-1] # get year from folder path
      file_paths[year] = folder_paths
  return file_paths

file_paths: Dict[str, List[str]] = init_file_paths(folders)

def parse_pdf(file_paths: Dict[str, List[str]]) -> Dict[str, List[str]]:
    all_transactions = {}
    for year, paths in file_paths.items(): # hopefully this gets the key and items.
        for path in paths:
            pdf_transactions: Optional[List[Dict[str, str | float]]] = None
            with pdfplumber.open(path) as pdf:
                # go page by page
                for page in pdf.pages:
                    text = page.extract_text()
                    if pdf_transactions:
                        pdf_transactions.extend(extract_transactions(text))
                    else:
                        pdf_transactions = extract_transactions(text)
                pdf.close()
            if pdf_transactions:
                # Don't get from the file_name. Get directly from the file. (Complex, add only when large scale)
                date_from_pdfname = re.compile(r'([a-zA-z]{3,4} \d{2})')
                name_of_pdf = date_from_pdfname.findall(path.split('/')[-1].replace('.pdf', ''))
                if name_of_pdf:
                    name_of_pdf = name_of_pdf[0]
                    all_transactions[name_of_pdf] = pdf_transactions
                else:
                    raise ValueError(f"No date found in {path}")
            else:
                raise ValueError(f"No transactions found in {path}")
    return all_transactions

def output_to_csv(all_transactions: Dict[str, List[Dict[str, str | float]]]):
    for name_of_pdf, transactions in all_transactions.items():
        df = pd.DataFrame(transactions)
        df.to_csv(f"{name_of_pdf}.csv", index=False)

if __name__ == "__main__":
    all_transactions = parse_pdf(file_paths)
    # output_to_csv(all_transactions)

"""
first_pdf_name = list(all_transactions.keys())[0]
transactions = all_transactions[first_pdf_name]
df = pd.DataFrame(transactions)
print(df)
"""
# output_to_csv(all_transactions)
